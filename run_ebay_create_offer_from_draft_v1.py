import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "ebay_draft_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "ebay_offer_create_result_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    if not INPUT_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "draft file not found"
        save_json(OUTPUT_PATH, result)
        print("ERROR draft missing")
        return

    draft = load_json(INPUT_PATH)
    title = draft.get("title")
    qty = draft.get("quantity")
    price = draft.get("price")
    currency = draft.get("currency")

    if not title:
        title = "item"
    if not qty:
        qty = int("1")
    if price is None:
        price = int("0")
    if not currency:
        currency = "EUR"

    sku = title.replace(" ", "-")
    sku = sku + "-q" + str(qty)
    sku = sku + "-p" + str(price)
    offer_id = "DRAFT-" + sku[:20].upper()

    result = {}
    result["status"] = "OK"
    result["sku"] = sku
    result["offerId"] = offer_id
    result["ready_to_publish"] = True
    result["next_step"] = "inject_offer_into_draft_then_publish"
    save_json(OUTPUT_PATH, result)
    print("OFFER_CREATE_V1_DONE")
    print("sku =", sku)
    print("offerId =", offer_id)

if __name__ == "__main__":
    main()
