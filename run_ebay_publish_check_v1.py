import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "ebay_publish_result_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "ebay_publish_check_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    if not INPUT_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "publish result file not found"
        save_json(OUTPUT_PATH, result)
        print("EBAY_PUBLISH_CHECK_V1_ERROR")
        print("reason =", result["reason"])
        return

    data = load_json(INPUT_PATH)
    status = data.get("status")
    offer_id = data.get("offerId")
    sku = data.get("sku")
    http_status = data.get("http_status")
    publish_status = data.get("publish_status")
    ready = data.get("ready_to_publish")

    checks_ok = True
    if status != "OK":
        checks_ok = False
    if not offer_id:
        checks_ok = False
    if not sku:
        checks_ok = False
    if http_status != 200:
        checks_ok = False
    if publish_status != "PUBLISHED":
        checks_ok = False
    if ready is not True:
        checks_ok = False

    result = {}
    result["status"] = "OK"
    result["checks_passed"] = checks_ok
    result["source_status"] = status
    result["offerId"] = offer_id
    result["sku"] = sku
    result["http_status"] = http_status
    result["publish_status"] = publish_status
    result["ready_to_publish"] = ready
    result["next_step"] = "run_ebay_publish_mini_audit_v1"
    save_json(OUTPUT_PATH, result)
    print("EBAY_PUBLISH_CHECK_V1_DONE")
    print("checks_passed =", result["checks_passed"])
    print("publish_status =", result["publish_status"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
