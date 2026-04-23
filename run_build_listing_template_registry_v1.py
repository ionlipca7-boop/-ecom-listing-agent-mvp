import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "multi_listing_layer_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "listing_template_registry_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    baseline_sku = source.get("baseline_sku")
    baseline_offer_id = source.get("baseline_offer_id")
    baseline_image_count = source.get("baseline_image_count", 0)
    result = {
        "status": "OK",
        "decision": "listing_template_registry_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "listing_template_registry_version": "v1",
        "baseline_template": {
            "template_key": "baseline_template_v1",
            "source_phase": source.get("source_phase"),
            "baseline_sku": baseline_sku,
            "baseline_offer_id": baseline_offer_id,
            "baseline_image_count": baseline_image_count,
            "reuse_photo_pipeline": True,
            "reuse_full_payload_rules": True,
            "inventory_first_then_offer": True,
            "read_after_each_update": True
        },
        "template_modes": [
            "baseline_clone",
            "variant_listing",
            "new_product_from_template" 
        ],
        "live_write_now": False,
        "next_step": "build_multi_listing_payload_builder_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("LISTING_TEMPLATE_REGISTRY_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = listing_template_registry_v1_built")
    print("template_key =", result["baseline_template"]["template_key"])
    print("baseline_image_count =", result["baseline_template"]["baseline_image_count"])
    print("reuse_photo_pipeline =", result["baseline_template"]["reuse_photo_pipeline"])
    print("live_write_now =", result["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
