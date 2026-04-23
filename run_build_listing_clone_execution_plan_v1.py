import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "multi_listing_payload_builder_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "listing_clone_execution_plan_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    result = {
        "status": "OK",
        "decision": "listing_clone_execution_plan_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "listing_clone_execution_plan_version": "v1",
        "template_key": source.get("template_key"),
        "baseline_sku": source.get("baseline_sku"),
        "baseline_offer_id": source.get("baseline_offer_id"),
        "baseline_image_count": source.get("baseline_image_count", 0),
        "execution_modes": {
            "baseline_clone": [
                "read_baseline_inventory",
                "build_full_inventory_payload",
                "apply_inventory_to_new_sku",
                "read_new_inventory_back",
                "build_offer_payload",
                "apply_offer_after_inventory_ok",
                "read_offer_back",
                "archive_result" 
            ],
            "variant_listing": [
                "read_baseline_inventory",
                "change_title_price_variant_fields",
                "preserve_working_images",
                "apply_full_inventory_payload",
                "read_inventory_back",
                "apply_offer_if_needed",
                "read_offer_back",
                "archive_result" 
            ],
            "new_product_from_template": [
                "create_new_registry_key",
                "assign_new_sku",
                "build_inventory_from_template",
                "read_inventory_back",
                "build_offer_from_template",
                "read_offer_back",
                "archive_result" 
            ]
        },
        "global_execution_rules": {
            "inventory_first_then_offer": True,
            "full_payload_only": True,
            "read_after_each_update": True,
            "preserve_working_images": True,
            "archive_after_success": True,
            "live_write_now": False
        },
        "next_step": "build_archive_and_github_sync_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("LISTING_CLONE_EXECUTION_PLAN_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = listing_clone_execution_plan_v1_built")
    print("template_key =", result["template_key"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("baseline_clone_steps =", len(result["execution_modes"]["baseline_clone"]))
    print("variant_listing_steps =", len(result["execution_modes"]["variant_listing"]))
    print("archive_after_success =", result["global_execution_rules"]["archive_after_success"])
    print("live_write_now =", result["global_execution_rules"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
