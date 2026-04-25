import json
import sys
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OFFER_ID = "152921341011"
API_URL = "https://api.ebay.com/sell/inventory/v1/offer/" + OFFER_ID + "/publish"
OUTPUT_FILE = EXPORTS_DIR / "ebay_publish_offer_audit_v4.json"

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").strip()

def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {"raw_text": response.text}

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")

    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }

    response = requests.post(API_URL, headers=headers, timeout=60)
    data = safe_json(response)

    result = {
        "status": "OK" if response.status_code == 200 else "FAILED",
        "http_status": response.status_code,
        "offerId": OFFER_ID,
        "listingId": data.get("listingId") if isinstance(data, dict) else None,
        "response_json": data
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("PUBLISH_OFFER_V4_DONE")
    print("http_status =", response.status_code)
    print("offerId =", OFFER_ID)
    if response.status_code == 200:
        print("listingId =", data.get("listingId"))
    if response.status_code != 200:
        if isinstance(data, dict) and data.get("errors"):
            first = data["errors"][0]
            print("first_error_code =", first.get("errorId"))
            print("first_error_message =", first.get("message"))
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
