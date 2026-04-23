import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "apply_fix_payload_v1.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "patch_auto_approve_v1.json"
UPDATED_PAYLOAD_FILE = BASE_DIR / "storage" / "exports" / "apply_fix_payload_v1_approved.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def safe_read_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return True, data, None
    except FileNotFoundError:
        return False, None, "input file not found: " + str(path)
    except json.JSONDecodeError as exc:
        return False, None, "invalid json: " + str(exc)
    except Exception as exc:
        return False, None, "unexpected read error: " + str(exc)

def main():
    ok, data, error = safe_read_json(INPUT_FILE)
    result = {}
    zero = int("0")
    one = int("1")
    result["approved_at"] = utc_now()
    result["source_file"] = str(INPUT_FILE)
    result["output_file"] = str(OUTPUT_FILE)
    result["updated_payload_file"] = str(UPDATED_PAYLOAD_FILE)
    result["approval_status"] = "READY"
    result["patch_count"] = zero
    result["approved_count"] = zero
    result["skipped_count"] = zero
    result["next_step"] = "RUN_PATCH_APPLIER"
    if not ok:
        result["approval_status"] = "ERROR"
        result["error"] = error
        result["next_step"] = "FIX_APPLY_FIX_PAYLOAD_INPUT"
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PATCH_AUTO_APPROVE_V1:")
        print("approval_status:", result["approval_status"])
        print("error:", error)
        print("output_file:", OUTPUT_FILE.name)
        return
    patches = data.get("patches", [])
    result["patch_count"] = len(patches)
    approved_count = zero
    skipped_count = zero
    for patch in patches:
        mode = patch.get("apply_mode")
        if mode == "PENDING_REVIEW":
            patch["apply_mode"] = "APPROVED"
            patch["approved_at"] = result["approved_at"]
            patch["approval_source"] = "AUTO_APPROVE_V1"
            approved_count = approved_count + one
        else:
            skipped_count = skipped_count + one
    result["approved_count"] = approved_count
    result["skipped_count"] = skipped_count
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    UPDATED_PAYLOAD_FILE.parent.mkdir(parents=True, exist_ok=True)
    UPDATED_PAYLOAD_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PATCH_AUTO_APPROVE_V1:")
    print("approval_status:", result["approval_status"])
    print("patch_count:", result["patch_count"])
    print("approved_count:", result["approved_count"])
    print("skipped_count:", result["skipped_count"])
    print("next_step:", result["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
