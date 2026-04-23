import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVE_PATH = BASE_DIR / "storage" / "memory" / "archive" / "photo_pipeline_v1_archive.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "multi_listing_layer_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(ARCHIVE_PATH)
    image_count = source.get("current_state", {}).get("image_count", 0)
    result = {
        "status": "OK",
        "decision": "multi_listing_layer_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "multi_listing_layer_version": "v1",
        "source_phase": source.get("phase"),
        "baseline_sku": source.get("sku"),
        "baseline_offer_id": source.get("offer_id"),
        "baseline_image_count": image_count,
        "layer_contract": {
            "reuse_photo_pipeline": True,
            "reuse_full_payload_rules": True,
            "inventory_first_then_offer": True,
            "read_after_each_update": True,
            "live_write_now": False
        },
        "listing_modes": [
            "baseline_clone",
            "variant_listing",
            "new_product_from_template" 
        ],
        "required_future_layers": [
            "listing_template_registry_v1",
            "multi_listing_payload_builder_v1",
            "listing_clone_execution_plan_v1",
            "archive_and_github_sync_v1" 
        ],
        "next_step": "build_listing_template_registry_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("MULTI_LISTING_LAYER_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = multi_listing_layer_v1_built")
    print("baseline_sku =", result["baseline_sku"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("reuse_photo_pipeline =", result["layer_contract"]["reuse_photo_pipeline"])
    print("live_write_now =", result["layer_contract"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
