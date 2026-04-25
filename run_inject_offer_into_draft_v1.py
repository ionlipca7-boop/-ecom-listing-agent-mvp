import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
DRAFT_PATH = EXPORTS_DIR / "ebay_draft_v1.json"
OFFER_PATH = EXPORTS_DIR / "ebay_offer_create_result_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "ebay_draft_with_offer_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    if not DRAFT_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "draft file not found"
        save_json(OUTPUT_PATH, result)
        print("INJECT_OFFER_V1_ERROR")
        print("reason =", result["reason"])
        return
    if not OFFER_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "offer result file not found"
        save_json(OUTPUT_PATH, result)
        print("INJECT_OFFER_V1_ERROR")
        print("reason =", result["reason"])
        return

    draft = load_json(DRAFT_PATH)
    offer = load_json(OFFER_PATH)

    draft["sku"] = offer.get("sku")
    draft["offerId"] = offer.get("offerId")
    draft["ready_to_publish"] = offer.get("ready_to_publish")
    draft["offer_source_status"] = offer.get("status")
    draft["next_step"] = "run_ebay_publish_draft_v1"

    save_json(OUTPUT_PATH, draft)
    print("INJECT_OFFER_V1_DONE")
    print("status = OK")
    print("sku =", draft["sku"])
    print("offerId =", draft["offerId"])
    print("ready_to_publish =", draft["ready_to_publish"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
