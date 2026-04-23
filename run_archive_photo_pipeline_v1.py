import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
ARCHIVE_DIR = BASE_DIR / "storage" / "memory" / "archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = ARCHIVE_DIR / "photo_pipeline_v1_archive.json"

def load_json(name):
    path = EXPORT_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    a = load_json("photo_upgrade_pipeline_v1.json")
    b = load_json("photo_source_registry_v1.json")
    c = load_json("photo_set_builder_v1.json")
    d = load_json("post_inventory_read_verification_v1.json")
    result = {
        "status": "OK",
        "decision": "photo_pipeline_v1_archived",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "phase": "PHOTO_PIPELINE_V1_READY",
        "sku": d.get("sku") or c.get("sku") or b.get("sku") or a.get("sku"),
        "offer_id": d.get("offer_id") or c.get("offer_id") or b.get("offer_id") or a.get("offer_id"),
        "achievements": [
            "photo_upgrade_pipeline_v1_built",
            "photo_source_registry_v1_built",
            "photo_set_builder_v1_built",
            "inventory_image_payload_builder_v1_built",
            "post_inventory_read_verification_v1_built" 
        ],
        "current_state": {
            "image_count": d.get("expected_image_count", 0),
            "safe_mode": True,
            "live_write_now": False,
            "full_payload_required": d.get("verification_contract", {}).get("require_full_payload_mode", False)
        },
        "rules": [
            "inventory_first_then_offer",
            "always_use_full_payload",
            "never_break_working_images",
            "eps_images_preferred",
            "always_read_after_inventory_update" 
        ],
        "next_priority": "build_multi_listing_layer_v1",
        "next_step": "build_multi_listing_layer_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ARCHIVE_PHOTO_PIPELINE_V1_AUDIT")
    print("status = OK")
    print("decision = photo_pipeline_v1_archived")
    print("sku =", result["sku"])
    print("image_count =", result["current_state"]["image_count"])
    print("safe_mode =", result["current_state"]["safe_mode"])
    print("live_write_now =", result["current_state"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
