import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def main():
    offer_path = EXPORT_DIR / "adapter_001_live_offer_v2.json"
    if not offer_path.exists():
        raise FileNotFoundError("Missing file: " + str(offer_path))
    live = read_json(offer_path)
    payload = {
        "sku": live.get("sku"),
        "marketplaceId": live.get("marketplaceId"),
        "format": live.get("format"),
        "availableQuantity": 12,
        "categoryId": live.get("categoryId"),
        "merchantLocationKey": live.get("merchantLocationKey"),
        "pricingSummary": {"price": {"value": "4.19", "currency": live.get("pricingSummary", {}).get("price", {}).get("currency", "EUR")}},
        "listingPolicies": dict(live.get("listingPolicies", {}))
    }
    result = {
        "status": "OK",
        "decision": "adapter_001_full_offer_update_v1_built",
        "offerId": live.get("offerId"),
        "sku": payload.get("sku"),
        "old_price": live.get("pricingSummary", {}).get("price", {}).get("value"),
        "new_price": payload.get("pricingSummary", {}).get("price", {}).get("value"),
        "old_quantity": live.get("availableQuantity"),
        "new_quantity": payload.get("availableQuantity"),
        "payload": payload
    }
    out_path = EXPORT_DIR / "adapter_001_full_offer_update_v1.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_FULL_OFFER_UPDATE_V1_OK")
    print("output =", str(out_path))
    print("decision =", result["decision"])
if __name__ == "__main__":
    main()
