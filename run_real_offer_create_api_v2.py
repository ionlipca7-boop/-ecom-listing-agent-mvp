import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "real_offer_request_payload_v3.json"
OUTPUT_PATH = EXPORTS_DIR / "real_offer_create_api_v2.json"

def main():
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
    data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    payload = data.get("payload", {})
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_DE"
    }
    url = "https://api.ebay.com/sell/inventory/v1/offer"
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    try:
        response_data = r.json()
    except Exception:
        response_data = {"raw_text": r.text[:4000]}
    offer_id = ""
    if isinstance(response_data, dict):
        offer_id = response_data.get("offerId", "")
    result = {
        "status": "OK" if r.status_code in [200, 201] else "FAILED",
        "decision": "real_offer_created" if offer_id else "real_offer_create_failed",
        "http_status": r.status_code,
        "offerId": offer_id,
        "request_payload": payload,
        "response": response_data
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("REAL_OFFER_CREATE_API_V2")
    print("http_status =", r.status_code)
    print("offerId =", offer_id)

if __name__ == "__main__":
    main()
