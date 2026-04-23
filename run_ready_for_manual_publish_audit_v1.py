import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "ready_for_manual_publish_audit_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    handoff = read_json(EXPORTS_DIR / "final_real_publish_handoff_v1.json")
    package_file = Path(str(handoff.get("payload_file", "")))
    manifest_file = Path(str(handoff.get("manifest_file", "")))
    package_dir = Path(str(handoff.get("package_dir", "")))

    handoff_ready = handoff.get("final_publish_handoff_status") == "READY"
    package_dir_exists = package_dir.exists() if str(package_dir) not in ("", ".") else False
    payload_exists = package_file.exists() if str(package_file) not in ("", ".") else False
    manifest_exists = manifest_file.exists() if str(manifest_file) not in ("", ".") else False

    all_ok = handoff_ready and package_dir_exists and payload_exists and manifest_exists

    result = {
        "checked_at": utc_now(),
        "audit_status": "PASS" if all_ok else "FAIL",
        "next_step": "SAFE_FOR_MANUAL_REAL_PUBLISH" if all_ok else "FIX_MISSING_ARTIFACTS",
        "handoff_status": handoff.get("final_publish_handoff_status"),
        "variant_id": handoff.get("variant_id"),
        "title": handoff.get("title"),
        "package_id": handoff.get("package_id"),
        "package_dir_exists": package_dir_exists,
        "payload_exists": payload_exists,
        "manifest_exists": manifest_exists
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("READY_FOR_MANUAL_PUBLISH_AUDIT_V1:")
    print("audit_status:", result["audit_status"])
    print("next_step:", result["next_step"])
    print("package_id:", result["package_id"])
    print("payload_exists:", result["payload_exists"])
    print("manifest_exists:", result["manifest_exists"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
