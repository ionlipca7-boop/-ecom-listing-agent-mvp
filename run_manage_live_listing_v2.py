import json
import requests
from pathlib import Path
BASE_DIR = Path(__file__).parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OFFER_ID = "152921341011"
NEW_PRICE = "13.49"
NEW_QUANTITY = 10
API_URL = "https://api.ebay.com/sell/inventory/v1/offer/"
OUTPUT_FILE = EXPORTS_DIR / "ebay_manage_listing_audit_v2.json"
def read_token():
    return (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8-sig").strip()
def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_token()
    url = API_URL + OFFER_ID
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}
    payload = {"pricingSummary": {"price": {"value": NEW_PRICE, "currency": "EUR"}}, "availableQuantity": NEW_QUANTITY}
    response = requests.patch(url, headers=headers, json=payload, timeout=60)
    result = {"status": "OK" if response.status_code == 204 else "FAILED", "http_status": response.status_code, "offerId": OFFER_ID, "price": NEW_PRICE, "quantity": NEW_QUANTITY, "response": response.text}
    OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("MANAGE_LISTING_V2_DONE")
    print("http_status =", response.status_code)
if __name__ == "__main__":
    main()
