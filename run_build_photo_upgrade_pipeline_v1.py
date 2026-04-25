import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVE_PATH = BASE_DIR / "storage" / "memory" / "archive" / "improved_baseline_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "photo_upgrade_pipeline_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    archive = load_json(ARCHIVE_PATH)
    current_state = archive.get("current_state", {})
    result = {
        "status": "OK",
        "decision": "photo_upgrade_pipeline_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "source_phase": archive.get("phase"),
        "sku": archive.get("sku"),
        "offer_id": archive.get("offer_id"),
        "current_image_count": current_state.get("image_count", 0),
        "current_title": current_state.get("title", ""),
        "photo_pipeline_version": "v1",
        "pipeline_rules": [
            "read_inventory_before_any_photo_change",
            "preserve_working_eps_images",
            "never_send_partial_inventory_payload",
            "inventory_first_then_offer_read",
            "work_through_full_payload_only",
            "prepare_multi_listing_ready_image_sets" 
        ],
        "planned_layers": [
            "photo_source_registry",
            "photo_set_builder",
            "inventory_image_payload_builder",
            "post_update_inventory_read",
            "multi_listing_image_reuse_map" 
        ],
        "next_runtime_targets": {
            "safe_mode": True,
            "live_write_now": False,
            "preserve_existing_image_count": True,
            "target_multi_listing_system": True
        },
        "next_step": "build_photo_source_registry_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PHOTO_UPGRADE_PIPELINE_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = photo_upgrade_pipeline_v1_built")
    print("sku =", result["sku"])
    print("offer_id =", result["offer_id"])
    print("current_image_count =", result["current_image_count"])
    print("safe_mode =", result["next_runtime_targets"]["safe_mode"])
    print("live_write_now =", result["next_runtime_targets"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
