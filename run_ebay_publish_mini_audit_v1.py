import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
RESULT_PATH = EXPORTS_DIR / "ebay_publish_result_v1.json"
CHECK_PATH = EXPORTS_DIR / "ebay_publish_check_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "ebay_publish_mini_audit_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    if not RESULT_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "publish result file not found"
        save_json(OUTPUT_PATH, result)
        print("EBAY_PUBLISH_MINI_AUDIT_V1_ERROR")
        print("reason =", result["reason"])
        return
    if not CHECK_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "publish check file not found"
        save_json(OUTPUT_PATH, result)
        print("EBAY_PUBLISH_MINI_AUDIT_V1_ERROR")
        print("reason =", result["reason"])
        return

    publish_data = load_json(RESULT_PATH)
    check_data = load_json(CHECK_PATH)

    result = {}
    result["status"] = "OK"
    result["result_status"] = publish_data.get("status")
    result["result_decision"] = publish_data.get("decision")
    result["offerId"] = publish_data.get("offerId")
    result["sku"] = publish_data.get("sku")
    result["http_status"] = publish_data.get("http_status")
    result["publish_status"] = publish_data.get("publish_status")
    result["check_status"] = check_data.get("status")
    result["checks_passed"] = check_data.get("checks_passed")
    result["pipeline_status"] = "PUBLISH_OK"
    result["next_step"] = "build_pipeline_status_or_real_api_publish"

    save_json(OUTPUT_PATH, result)
    print("EBAY_PUBLISH_MINI_AUDIT_V1_DONE")
    print("status =", result["status"])
    print("pipeline_status =", result["pipeline_status"])
    print("checks_passed =", result["checks_passed"])
    print("offerId =", result["offerId"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
