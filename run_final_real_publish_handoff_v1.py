import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "final_real_publish_handoff_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def pick_first(*values):
    for value in values:
        if value not in (None, ""):
            return value
    return None

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    handoff_data = read_json(EXPORTS_DIR / "variant_handoff_v1.json")
    global_data = read_json(EXPORTS_DIR / "global_master_status_v1.json")
    package_data = read_json(EXPORTS_DIR / "publish_package_from_variant_v1.json")
    execution_export_data = read_json(EXPORTS_DIR / "execution_variant_export_v1.json")

    global_summary = global_data.get("summary", {})
    execution_payload = execution_export_data.get("execution_payload", {})

    handoff_status = handoff_data.get("handoff_status", "")
    system_status = global_data.get("system_status", "")
    upload_status = global_summary.get("upload_status", "")

    variant_id = pick_first(handoff_data.get("variant_id"), package_data.get("selected_variant_id"), global_summary.get("selected_variant_id"))
    title = pick_first(handoff_data.get("title"), package_data.get("selected_title"), execution_payload.get("Title"))
    price = pick_first(handoff_data.get("price"), execution_payload.get("Price"))
    angle = pick_first(handoff_data.get("angle"), execution_payload.get("SelectedAngle"))
    package_id = pick_first(handoff_data.get("package_id"), package_data.get("package_id"), global_summary.get("package_id"))
    package_dir = package_data.get("package_dir")
    payload_file = package_data.get("payload_file")
    manifest_file = package_data.get("manifest_file")

    is_ready = handoff_status == "READY" and system_status == "READY" and variant_id is not None and title is not None and package_id is not None

    result = {
        "checked_at": utc_now(),
        "final_publish_handoff_status": "READY" if is_ready else "BLOCKED",
        "next_step": "MANUAL_REAL_PUBLISH" if is_ready else "FIX_PREVIOUS_LAYER",
        "variant_id": variant_id,
        "title": title,
        "price": price,
        "angle": angle,
        "package_id": package_id,
        "package_dir": package_dir,
        "payload_file": payload_file,
        "manifest_file": manifest_file,
        "upload_status": upload_status,
        "system_status": system_status
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("FINAL_REAL_PUBLISH_HANDOFF_V1:")
    print("final_publish_handoff_status:", result["final_publish_handoff_status"])
    print("next_step:", result["next_step"])
    print("variant_id:", result["variant_id"])
    print("package_id:", result["package_id"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
