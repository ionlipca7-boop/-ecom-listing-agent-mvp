import json
import requests
from pathlib import Path
BASE = Path(__file__).resolve().parent
TOKEN_PATH = BASE / "storage" / "secrets" / "ebay_access_token.txt"
OFFER_PATH = BASE / "storage" / "exports" / "ebay_update_offer_audit_v2.json"
def get_token():
    return TOKEN_PATH.read_text(encoding="utf-8").strip()
def get_offer_id():
    data = json.loads(OFFER_PATH.read_text(encoding="utf-8"))
    return data.get("offerId")
def main():
    offer_id = get_offer_id()
    url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}"
    payload = {
        "pricingSummary": {
            "price": {
                "value": "4.99",
                "currency": "EUR"
            }
        }
    }
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }
    r = requests.put(url, headers=headers, json=payload)
    print("OFFER_UPDATE_AUTO_V2")
    print("offer_id =", offer_id)
    print("http_status =", r.status_code)
    try:
        print("response =", r.json())
    except:
        print("response_text =", r.text)
if __name__ == "__main__":
    main()
