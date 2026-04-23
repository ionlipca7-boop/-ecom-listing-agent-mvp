import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "variant_handoff_v1.json"

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

    execution_data = read_json(EXPORTS_DIR / "execution_control_room_v1.json")
    publish_data = read_json(EXPORTS_DIR / "publish_variant_control_room_v1.json")
    global_data = read_json(EXPORTS_DIR / "global_master_status_v1.json")
    variant_data = read_json(EXPORTS_DIR / "variant_selector_v1.json")
    execution_export_data = read_json(EXPORTS_DIR / "execution_variant_export_v1.json")
    package_data = read_json(EXPORTS_DIR / "publish_package_from_variant_v1.json")

    variant_summary = variant_data.get("summary", {})
    selected_variant = variant_data.get("selected_variant", {})
    execution_summary = execution_export_data.get("summary", {})
    execution_payload = execution_export_data.get("execution_payload", {})
    publish_summary = publish_data.get("summary", {})
    global_summary = global_data.get("summary", {})

    execution_status = pick_first(execution_data.get("execution_status"), global_summary.get("execution_status"))
    publish_status = pick_first(publish_data.get("publish_variant_status"), global_summary.get("publish_status"), publish_summary.get("package_status"))
    system_status = global_data.get("system_status", "")

    variant_id = pick_first(selected_variant.get("variant_id"), variant_summary.get("selected_variant_id"), execution_summary.get("selected_variant_id"), execution_payload.get("SelectedVariantID"), package_data.get("selected_variant_id"), publish_summary.get("selected_variant_id"), global_summary.get("selected_variant_id"))
    title = pick_first(selected_variant.get("title"), variant_summary.get("selected_title"), execution_summary.get("selected_title"), execution_payload.get("Title"), package_data.get("selected_title"), publish_summary.get("selected_title"))
    price = pick_first(selected_variant.get("price"), variant_summary.get("selected_price"), execution_summary.get("selected_price"), execution_payload.get("Price"))
    angle = pick_first(selected_variant.get("angle"), variant_summary.get("selected_angle"), execution_payload.get("SelectedAngle"))
    package_id = pick_first(package_data.get("package_id"), publish_summary.get("package_id"), global_summary.get("package_id"))

    is_ready = execution_status == "READY" and publish_status == "READY" and system_status == "READY" and variant_id is not None and title is not None

    result = {
        "checked_at": utc_now(),
        "handoff_status": "READY" if is_ready else "BLOCKED",
        "next_step": "FINAL_REAL_PUBLISH_HANDOFF" if is_ready else "FIX_PREVIOUS_LAYER",
        "variant_id": variant_id,
        "title": title,
        "price": price,
        "angle": angle,
        "package_id": package_id,
        "execution_status": execution_status,
        "publish_status": publish_status,
        "system_status": system_status
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("VARIANT_HANDOFF_V1:")
    print("handoff_status:", result["handoff_status"])
    print("next_step:", result["next_step"])
    print("variant_id:", result["variant_id"])
    print("title:", result["title"])
    print("package_id:", result["package_id"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
