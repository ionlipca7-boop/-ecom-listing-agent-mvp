import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "inventory_image_payload_builder_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "post_inventory_read_verification_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    result = {
        "status": "OK",
        "decision": "post_inventory_read_verification_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "post_inventory_read_verification_version": "v1",
        "sku": source.get("sku"),
        "offer_id": source.get("offer_id"),
        "expected_image_count": source.get("image_count", 0),
        "verification_contract": {
            "read_after_inventory_update": True,
            "compare_image_count": True,
            "compare_sku": True,
            "preserve_existing_images": True,
            "require_full_payload_mode": True,
            "live_write_now": False
        },
        "verification_targets": [
            "sku",
            "product.imageUrls",
            "image_count",
            "inventory_payload_integrity" 
        ],
        "next_step": "archive_photo_pipeline_v1_and_prepare_multi_listing_layer" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("POST_INVENTORY_READ_VERIFICATION_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = post_inventory_read_verification_v1_built")
    print("sku =", result["sku"])
    print("expected_image_count =", result["expected_image_count"])
    print("read_after_inventory_update =", result["verification_contract"]["read_after_inventory_update"])
    print("require_full_payload_mode =", result["verification_contract"]["require_full_payload_mode"])
    print("live_write_now =", result["verification_contract"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
