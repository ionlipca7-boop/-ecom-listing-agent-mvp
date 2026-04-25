import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
ARCHIVE_DIR = BASE_DIR / "storage" / "memory" / "archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = ARCHIVE_DIR / "multi_listing_system_v1_archive.json"

def load_json(name):
    path = EXPORT_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    a = load_json("multi_listing_layer_v1.json")
    b = load_json("listing_template_registry_v1.json")
    c = load_json("multi_listing_payload_builder_v1.json")
    d = load_json("listing_clone_execution_plan_v1.json")
    e = load_json("archive_and_github_sync_v1.json")
    result = {
        "status": "OK",
        "decision": "multi_listing_system_v1_archived",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "phase": "MULTI_LISTING_SYSTEM_V1_READY",
        "template_key": e.get("template_key") or d.get("template_key") or c.get("template_key"),
        "baseline_sku": e.get("baseline_sku") or d.get("baseline_sku") or c.get("baseline_sku"),
        "baseline_offer_id": e.get("baseline_offer_id") or d.get("baseline_offer_id") or c.get("baseline_offer_id"),
        "baseline_image_count": e.get("baseline_image_count", 0),
        "achievements": [
            "multi_listing_layer_v1_built",
            "listing_template_registry_v1_built",
            "multi_listing_payload_builder_v1_built",
            "listing_clone_execution_plan_v1_built",
            "archive_and_github_sync_v1_built" 
        ],
        "current_state": {
            "baseline_image_count": e.get("baseline_image_count", 0),
            "baseline_clone_ready": c.get("payload_modes", {}).get("baseline_clone", {}).get("enabled", False),
            "variant_listing_ready": c.get("payload_modes", {}).get("variant_listing", {}).get("enabled", False),
            "archive_ready": e.get("archive_contract", {}).get("save_local_archive", False),
            "github_backup_ready": e.get("github_sync_contract", {}).get("github_sync_ready", False),
            "auto_push_now": e.get("github_sync_contract", {}).get("auto_push_now", False)
        },
        "rules": [
            "inventory_first_then_offer",
            "always_use_full_payload",
            "always_read_after_each_update",
            "preserve_working_images",
            "archive_after_success",
            "github_as_backup_not_runtime" 
        ],
        "next_priority": "prepare_first_real_multi_listing_run_v1",
        "next_step": "prepare_first_real_multi_listing_run_v1" 
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ARCHIVE_MULTI_LISTING_SYSTEM_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = multi_listing_system_v1_archived")
    print("template_key =", result["template_key"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("baseline_clone_ready =", result["current_state"]["baseline_clone_ready"])
    print("variant_listing_ready =", result["current_state"]["variant_listing_ready"])
    print("github_backup_ready =", result["current_state"]["github_backup_ready"])
    print("auto_push_now =", result["current_state"]["auto_push_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
