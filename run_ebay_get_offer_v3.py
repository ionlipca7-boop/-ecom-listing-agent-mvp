import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OFFER_ID = "152921341011"
API_URL = "https://api.ebay.com/sell/inventory/v1/offer/" + OFFER_ID
OUTPUT_FILE = EXPORTS_DIR / "ebay_get_offer_audit_v3.json"

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Language": "de-DE"}
    response = requests.get(API_URL, headers=headers, timeout=60)
    data = response.json()
    result = {"http_status": response.status_code, "offerId": OFFER_ID, "response_json": data}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("GET_OFFER_V3_DONE")
    print("http_status =", response.status_code)
    print("offerId =", OFFER_ID)

if __name__ == "__main__":
    main()
