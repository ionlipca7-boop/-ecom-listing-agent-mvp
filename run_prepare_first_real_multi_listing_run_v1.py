import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "memory" / "archive" / "multi_listing_system_v1_archive.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "prepare_first_real_multi_listing_run_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    result = {
        "status": "OK",
        "decision": "prepare_first_real_multi_listing_run_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "prepare_first_real_multi_listing_run_version": "v1",
        "template_key": source.get("template_key"),
        "baseline_sku": source.get("baseline_sku"),
        "baseline_offer_id": source.get("baseline_offer_id"),
        "baseline_image_count": source.get("baseline_image_count", 0),
        "selected_mode": "baseline_clone",
        "run_contract": {
            "mode_ready": True,
            "baseline_clone_ready": source.get("current_state", {}).get("baseline_clone_ready", False),
            "variant_listing_ready": source.get("current_state", {}).get("variant_listing_ready", False),
            "github_backup_ready": source.get("current_state", {}).get("github_backup_ready", False),
            "auto_push_now": source.get("current_state", {}).get("auto_push_now", False),
            "live_publish_now": False
        },
        "required_runtime_inputs": [
            "new_registry_key",
            "new_sku",
            "target_title",
            "target_price",
            "category_id",
            "merchant_location_key",
            "fulfillment_policy_id",
            "payment_policy_id",
            "return_policy_id" 
        ],
        "pre_run_checks": [
            "confirm_baseline_inventory_read",
            "confirm_full_payload_mode",
            "confirm_image_count_match",
            "confirm_policy_ids_present",
            "confirm_new_sku_not_empty",
            "confirm_archive_after_success" 
        ],
        "next_step": "build_first_real_multi_listing_input_stub_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PREPARE_FIRST_REAL_MULTI_LISTING_RUN_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = prepare_first_real_multi_listing_run_v1_built")
    print("template_key =", result["template_key"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("selected_mode =", result["selected_mode"])
    print("baseline_clone_ready =", result["run_contract"]["baseline_clone_ready"])
    print("live_publish_now =", result["run_contract"]["live_publish_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
