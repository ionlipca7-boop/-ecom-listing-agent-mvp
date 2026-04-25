import json
import sys
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
LIVE_SKU = "ECOM-TEST-CABLE-001"
LIVE_OFFER_ID = "152921341011"
NEW_TOTAL_QTY = 20
NEW_OFFER_QTY = 20
API_URL = "https://api.ebay.com/sell/inventory/v1/bulk_update_price_quantity"
OUTPUT_FILE = EXPORTS_DIR / "ebay_increase_live_quantity_audit_v1.json"

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {"raw_text": response.text}

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    payload = {"requests": [{"sku": LIVE_SKU, "shipToLocationAvailability": {"quantity": NEW_TOTAL_QTY}, "offers": [{"offerId": LIVE_OFFER_ID, "availableQuantity": NEW_OFFER_QTY}]}]}
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    data = safe_json(response)
    result = {"status": "OK" if response.status_code == 200 else "FAILED", "http_status": response.status_code, "sku": LIVE_SKU, "offerId": LIVE_OFFER_ID, "request_payload": payload, "response_json": data}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("INCREASE_LIVE_QUANTITY_V1_DONE")
    print("http_status =", response.status_code)
    print("sku =", LIVE_SKU)
    print("offerId =", LIVE_OFFER_ID)
    if response.status_code != 200:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
