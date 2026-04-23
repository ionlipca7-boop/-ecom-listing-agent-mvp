import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "ebay_draft_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "ebay_draft_diagnose_v1.json"
def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
def main():
    if not INPUT_PATH.exists():
        result = {"status": "ERROR", "reason": "draft file not found", "input_path": str(INPUT_PATH)}
        save_json(OUTPUT_PATH, result)
        print("EBAY_DRAFT_DIAGNOSE_V1_ERROR")
        print("reason =", result["reason"])
        return
    d = load_json(INPUT_PATH)
    offer_id = d.get("offerId") or d.get("offer_id") or d.get("ebay_offer_id")
    sku = d.get("sku") or (d.get("product") or {}).get("sku")
    result = {
        "status": "OK",
        "input_path": str(INPUT_PATH),
        "has_offerId": bool(offer_id),
        "has_sku": bool(sku),
        "offerId": offer_id,
        "sku": sku,
        "main_title": d.get("main_title"),
        "price": d.get("price"),
        "draft_keys": sorted(list(d.keys())),
        "next_step": "publish_ready" if offer_id else "need_offer_creation_layer"
    }
    save_json(OUTPUT_PATH, result)
    print("EBAY_DRAFT_DIAGNOSE_V1_DONE")
    print("status =", result["status"])
    print("has_offerId =", result["has_offerId"])
    print("has_sku =", result["has_sku"])
    print("offerId =", result["offerId"])
    print("sku =", result["sku"])
    print("next_step =", result["next_step"])
if __name__ == "__main__":
    main()
