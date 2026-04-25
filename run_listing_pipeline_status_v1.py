import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
GENERATOR_PATH = EXPORTS_DIR / "generator_output_v5.json"
DRAFT_PATH = EXPORTS_DIR / "ebay_draft_v1.json"
PUBLISH_PATH = EXPORTS_DIR / "ebay_publish_result_v1.json"
PUBLISH_CHECK_PATH = EXPORTS_DIR / "ebay_publish_check_v1.json"
MINI_AUDIT_PATH = EXPORTS_DIR / "ebay_publish_mini_audit_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "listing_pipeline_status_v1.json"
def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
def safe_load(path):
    if not path.exists():
        return {}
    return load_json(path)
def main():
    generator_exists = GENERATOR_PATH.exists()
    draft_exists = DRAFT_PATH.exists()
    publish_exists = PUBLISH_PATH.exists()
    publish_check_exists = PUBLISH_CHECK_PATH.exists()
    mini_audit_exists = MINI_AUDIT_PATH.exists()
    generator = safe_load(GENERATOR_PATH)
    draft = safe_load(DRAFT_PATH)
    publish = safe_load(PUBLISH_PATH)
    publish_check = safe_load(PUBLISH_CHECK_PATH)
    mini_audit = safe_load(MINI_AUDIT_PATH)
    result = {
        "status": "OK",
        "overall_status": "PIPELINE_READY",
        "generator_exists": generator_exists,
        "draft_exists": draft_exists,
        "publish_exists": publish_exists,
        "publish_check_exists": publish_check_exists,
        "mini_audit_exists": mini_audit_exists,
        "generator_main_title": generator.get("main_title"),
        "generator_price": generator.get("price"),
        "draft_offerId": draft.get("offerId") or draft.get("offer_id") or draft.get("ebay_offer_id"),
        "draft_sku": draft.get("sku") or (draft.get("product") or {}).get("sku"),
        "publish_status": publish.get("status"),
        "publish_http_status": publish.get("http_status"),
        "publish_ready_to_publish": publish.get("ready_to_publish"),
        "publish_check_status": publish_check.get("status"),
        "publish_check_passed": publish_check.get("checks_passed"),
        "mini_audit_status": mini_audit.get("status"),
        "mini_audit_summary": mini_audit.get("summary"),
        "next_step": "",
        "notes": []
    }
    if not generator_exists:
        result["status"] = "WARN"
        result["overall_status"] = "GENERATOR_MISSING"
        result["next_step"] = "regenerate_generator_output_v5"
        result["notes"].append("generator_output_v5.json missing")
    elif not draft_exists:
        result["status"] = "WARN"
        result["overall_status"] = "DRAFT_MISSING"
        result["next_step"] = "rebuild_ebay_draft_v1"
        result["notes"].append("ebay_draft_v1.json missing")
    elif not publish_exists:
        result["status"] = "WARN"
        result["overall_status"] = "PUBLISH_RESULT_MISSING"
        result["next_step"] = "run_ebay_publish_draft_v1"
        result["notes"].append("ebay_publish_result_v1.json missing")
    elif publish.get("status") == "OK":
        result["overall_status"] = "PUBLISH_SUCCESS"
        result["next_step"] = "move_to_performance_or_dashboard_layer"
        result["notes"].append("publish completed successfully")
    elif publish.get("status") == "PREPARED":
        result["status"] = "WARN"
        result["overall_status"] = "PUBLISH_PREPARED_ONLY"
        result["next_step"] = "fix_offerId_or_token_then_rerun_publish"
        result["notes"].append("publish payload prepared but request not sent")
    elif publish.get("status") == "ERROR":
        result["status"] = "WARN"
        result["overall_status"] = "PUBLISH_ERROR"
        result["next_step"] = "inspect_publish_response_and_fix_api_layer"
        result["notes"].append("publish request failed")
    else:
        result["status"] = "WARN"
        result["overall_status"] = "UNKNOWN_STATE"
        result["next_step"] = "inspect_pipeline_files"
        result["notes"].append("unrecognized pipeline state")
    save_json(OUTPUT_PATH, result)
    print("LISTING_PIPELINE_STATUS_V1_DONE")
    print("status =", result["status"])
    print("overall_status =", result["overall_status"])
    print("publish_status =", result["publish_status"])
    print("publish_http_status =", result["publish_http_status"])
    print("next_step =", result["next_step"])
    print("output_file =", OUTPUT_PATH)
if __name__ == "__main__":
    main()
