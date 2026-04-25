import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "one_click_package_ready_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    manual_ready = read_json(EXPORTS_DIR / "manual_publish_ready_status_v1.json")
    assets_ready = read_json(EXPORTS_DIR / "attach_variant_package_assets_v1.json")
    final_handoff = read_json(EXPORTS_DIR / "final_real_publish_handoff_v1.json")

    manual_status = manual_ready.get("manual_publish_status", "")
    assets_status = assets_ready.get("attach_status", "")
    package_dir = final_handoff.get("package_dir", "")
    payload_file = final_handoff.get("payload_file", "")
    manifest_file = final_handoff.get("manifest_file", "")

    is_ready = manual_status == "READY" and assets_status == "READY"

    result = {
        "checked_at": utc_now(),
        "one_click_package_status": "READY" if is_ready else "BLOCKED",
        "next_step": "BUILD_SEMIAUTO_UPLOAD_LAYER" if is_ready else "FIX_PREVIOUS_LAYER",
        "package_id": final_handoff.get("package_id"),
        "variant_id": final_handoff.get("variant_id"),
        "title": final_handoff.get("title"),
        "price": final_handoff.get("price"),
        "package_dir": package_dir,
        "payload_file": payload_file,
        "manifest_file": manifest_file,
        "manual_publish_status": manual_status,
        "attach_assets_status": assets_status,
        "copied_count": assets_ready.get("copied_count", 0),
        "missing_count": assets_ready.get("missing_count", 0)
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("ONE_CLICK_PACKAGE_READY_V1:")
    print("one_click_package_status:", result["one_click_package_status"])
    print("next_step:", result["next_step"])
    print("package_id:", result["package_id"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
