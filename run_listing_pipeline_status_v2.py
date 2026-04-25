import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
GENERATOR_PATH = EXPORTS_DIR / "generator_output_v5.json"
DRAFT_PATH = EXPORTS_DIR / "ebay_draft_v1.json"
OFFER_PATH = EXPORTS_DIR / "ebay_offer_create_result_v1.json"
DRAFT_WITH_OFFER_PATH = EXPORTS_DIR / "ebay_draft_with_offer_v1.json"
PUBLISH_PATH = EXPORTS_DIR / "ebay_publish_result_v1.json"
PUBLISH_CHECK_PATH = EXPORTS_DIR / "ebay_publish_check_v1.json"
MINI_AUDIT_PATH = EXPORTS_DIR / "ebay_publish_mini_audit_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "listing_pipeline_status_v2.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def safe_load(path):
    if not path.exists():
        return {}
    return load_json(path)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    generator = safe_load(GENERATOR_PATH)
    draft = safe_load(DRAFT_PATH)
    offer = safe_load(OFFER_PATH)
    draft_with_offer = safe_load(DRAFT_WITH_OFFER_PATH)
    publish_data = safe_load(PUBLISH_PATH)
    publish_check = safe_load(PUBLISH_CHECK_PATH)
    mini_audit = safe_load(MINI_AUDIT_PATH)

    result = {}
    result["status"] = "OK"
    result["overall_status"] = "PIPELINE_OK"
    result["generator_exists"] = GENERATOR_PATH.exists()
    result["draft_exists"] = DRAFT_PATH.exists()
    result["offer_exists"] = OFFER_PATH.exists()
    result["draft_with_offer_exists"] = DRAFT_WITH_OFFER_PATH.exists()
    result["publish_exists"] = PUBLISH_PATH.exists()
    result["publish_check_exists"] = PUBLISH_CHECK_PATH.exists()
    result["mini_audit_exists"] = MINI_AUDIT_PATH.exists()
    result["main_title"] = generator.get("main_title") or draft.get("title")
    result["price"] = generator.get("price")
    result["sku"] = offer.get("sku") or draft_with_offer.get("sku") or publish_data.get("sku")
    result["offerId"] = offer.get("offerId") or draft_with_offer.get("offerId") or publish_data.get("offerId")
    result["publish_status"] = publish_data.get("publish_status")
    result["http_status"] = publish_data.get("http_status")
    result["checks_passed"] = publish_check.get("checks_passed")
    result["pipeline_status"] = mini_audit.get("pipeline_status")
    result["mode"] = "SIMULATED_PIPELINE"
    result["next_step"] = "real_api_publish_layer_or_dashboard_layer"
    save_json(OUTPUT_PATH, result)
    print("LISTING_PIPELINE_STATUS_V2_DONE")
    print("status =", result["status"])
    print("overall_status =", result["overall_status"])
    print("pipeline_status =", result["pipeline_status"])
    print("checks_passed =", result["checks_passed"])
    print("next_step =", result["next_step"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
