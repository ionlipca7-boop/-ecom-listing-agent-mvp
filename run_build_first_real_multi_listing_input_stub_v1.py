import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "prepare_first_real_multi_listing_run_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "first_real_multi_listing_input_stub_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    result = {
        "status": "OK",
        "decision": "first_real_multi_listing_input_stub_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "first_real_multi_listing_input_stub_version": "v1",
        "template_key": source.get("template_key"),
        "selected_mode": source.get("selected_mode"),
        "baseline_sku": source.get("baseline_sku"),
        "baseline_offer_id": source.get("baseline_offer_id"),
        "baseline_image_count": source.get("baseline_image_count", 0),
        "input_stub": {
            "new_registry_key": "REPLACE_ME_NEW_REGISTRY_KEY",
            "new_sku": "REPLACE_ME_NEW_SKU",
            "target_title": "REPLACE_ME_TARGET_TITLE",
            "target_price": "REPLACE_ME_TARGET_PRICE",
            "category_id": "REPLACE_ME_CATEGORY_ID",
            "merchant_location_key": "REPLACE_ME_LOCATION_KEY",
            "fulfillment_policy_id": "REPLACE_ME_FULFILLMENT_POLICY_ID",
            "payment_policy_id": "REPLACE_ME_PAYMENT_POLICY_ID",
            "return_policy_id": "REPLACE_ME_RETURN_POLICY_ID" 
        },
        "rules": {
            "inventory_first_then_offer": True,
            "full_payload_only": True,
            "read_after_each_update": True,
            "preserve_working_images": True,
            "live_publish_now": False
        },
        "next_step": "review_and_fill_first_real_multi_listing_input_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("FIRST_REAL_MULTI_LISTING_INPUT_STUB_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = first_real_multi_listing_input_stub_v1_built")
    print("template_key =", result["template_key"])
    print("selected_mode =", result["selected_mode"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("has_new_sku_field =", "new_sku" in result["input_stub"])
    print("live_publish_now =", result["rules"]["live_publish_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
