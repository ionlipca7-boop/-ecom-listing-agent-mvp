import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "listing_template_registry_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "multi_listing_payload_builder_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    baseline = source.get("baseline_template", {})
    baseline_image_count = baseline.get("baseline_image_count", 0)
    result = {
        "status": "OK",
        "decision": "multi_listing_payload_builder_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "multi_listing_payload_builder_version": "v1",
        "template_key": baseline.get("template_key"),
        "baseline_sku": baseline.get("baseline_sku"),
        "baseline_offer_id": baseline.get("baseline_offer_id"),
        "baseline_image_count": baseline_image_count,
        "payload_modes": {
            "baseline_clone": {
                "enabled": True,
                "reuse_images": True,
                "reuse_full_payload_rules": True
            },
            "variant_listing": {
                "enabled": True,
                "allow_title_changes": True,
                "allow_price_changes": True,
                "reuse_images": True
            },
            "new_product_from_template": {
                "enabled": True,
                "require_new_sku": True,
                "require_inventory_read_first": True,
                "reuse_photo_pipeline": True
            }
        },
        "global_rules": {
            "inventory_first_then_offer": True,
            "full_payload_only": True,
            "read_after_each_update": True,
            "preserve_working_images": True,
            "live_write_now": False
        },
        "next_step": "build_listing_clone_execution_plan_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("MULTI_LISTING_PAYLOAD_BUILDER_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = multi_listing_payload_builder_v1_built")
    print("template_key =", result["template_key"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("baseline_clone_enabled =", result["payload_modes"]["baseline_clone"]["enabled"])
    print("variant_listing_enabled =", result["payload_modes"]["variant_listing"]["enabled"])
    print("live_write_now =", result["global_rules"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
