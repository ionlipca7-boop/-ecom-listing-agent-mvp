import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "manual_publish_ready_status_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    audit_data = read_json(EXPORTS_DIR / "ready_for_manual_publish_audit_v1.json")
    handoff_data = read_json(EXPORTS_DIR / "final_real_publish_handoff_v1.json")

    audit_status = audit_data.get("audit_status", "")
    handoff_status = handoff_data.get("final_publish_handoff_status", "")

    is_ready = audit_status == "PASS" and handoff_status == "READY"

    result = {
        "checked_at": utc_now(),
        "manual_publish_status": "READY" if is_ready else "BLOCKED",
        "next_step": "OPEN_PACKAGE_AND_PUBLISH_MANUALLY" if is_ready else "FIX_PREVIOUS_LAYER",
        "variant_id": handoff_data.get("variant_id"),
        "title": handoff_data.get("title"),
        "price": handoff_data.get("price"),
        "package_id": handoff_data.get("package_id"),
        "package_dir": handoff_data.get("package_dir"),
        "payload_file": handoff_data.get("payload_file"),
        "manifest_file": handoff_data.get("manifest_file"),
        "audit_status": audit_status,
        "handoff_status": handoff_status
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("MANUAL_PUBLISH_READY_STATUS_V1:")
    print("manual_publish_status:", result["manual_publish_status"])
    print("next_step:", result["next_step"])
    print("package_id:", result["package_id"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
