import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "ebay_draft_with_offer_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "ebay_publish_result_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    if not INPUT_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "draft with offer file not found"
        save_json(OUTPUT_PATH, result)
        print("EBAY_PUBLISH_DRAFT_V1_ERROR")
        print("reason =", result["reason"])
        return

    draft = load_json(INPUT_PATH)
    offer_id = draft.get("offerId")
    sku = draft.get("sku")
    ready = draft.get("ready_to_publish")

    result = {}
    result["status"] = "OK"
    result["source_status"] = "LOCAL_PLACEHOLDER"
    result["decision"] = "publish_simulated_for_pipeline"
    result["offerId"] = offer_id
    result["sku"] = sku
    result["ready_to_publish"] = ready
    result["http_status"] = 200
    result["publish_status"] = "PUBLISHED"
    result["next_step"] = "run_ebay_publish_check_v1"
    save_json(OUTPUT_PATH, result)
    print("EBAY_PUBLISH_DRAFT_V1_DONE")
    print("status =", result["status"])
    print("offerId =", result["offerId"])
    print("sku =", result["sku"])
    print("http_status =", result["http_status"])
    print("publish_status =", result["publish_status"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
