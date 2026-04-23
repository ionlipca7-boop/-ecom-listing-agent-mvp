import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "apply_fix_payload_v1_approved.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "patch_applier_v1.json"
APPLIED_FILE = BASE_DIR / "storage" / "exports" / "applied_fix_result_v1.json"

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
    applied = {}
    zero = int("0")
    one = int("1")
    result["applied_at"] = utc_now()
    result["source_file"] = str(INPUT_FILE)
    result["output_file"] = str(OUTPUT_FILE)
    result["applied_file"] = str(APPLIED_FILE)
    result["applier_status"] = "READY"
    result["approved_patch_count"] = zero
    result["applied_count"] = zero
    result["skipped_count"] = zero
    result["next_step"] = "RUN_POST_FIX_VALIDATION"
    result["applied_fields"] = []
    applied["generated_at"] = result["applied_at"]
    applied["source_file"] = str(INPUT_FILE)
    applied["apply_status"] = "READY"
    applied["applied_patch_count"] = zero
    applied["fields"] = {}
    if not ok:
        result["applier_status"] = "ERROR"
        result["error"] = error
        result["next_step"] = "FIX_APPROVED_PAYLOAD_INPUT"
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        APPLIED_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        APPLIED_FILE.write_text(json.dumps(applied, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PATCH_APPLIER_V1:")
        print("applier_status:", result["applier_status"])
        print("error:", error)
        print("output_file:", OUTPUT_FILE.name)
        return
    patches = data.get("patches", [])
    result["approved_patch_count"] = len(patches)
    applied_count = zero
    skipped_count = zero
    for patch in patches:
        if patch.get("apply_mode") != "APPROVED":
            skipped_count = skipped_count + one
            continue
        field_name = patch.get("target_field", "unknown")
        applied["fields"][field_name] = patch.get("patch_value")
        result["applied_fields"].append(field_name)
        applied_count = applied_count + one
    result["applied_count"] = applied_count
    result["skipped_count"] = skipped_count
    applied["applied_patch_count"] = applied_count
    if applied_count == zero:
        result["applier_status"] = "NO_APPROVED_PATCHES"
        result["next_step"] = "REVIEW_APPROVAL_LAYER"
        applied["apply_status"] = "NO_APPROVED_PATCHES"
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    APPLIED_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    APPLIED_FILE.write_text(json.dumps(applied, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PATCH_APPLIER_V1:")
    print("applier_status:", result["applier_status"])
    print("approved_patch_count:", result["approved_patch_count"])
    print("applied_count:", result["applied_count"])
    print("skipped_count:", result["skipped_count"])
    print("next_step:", result["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
