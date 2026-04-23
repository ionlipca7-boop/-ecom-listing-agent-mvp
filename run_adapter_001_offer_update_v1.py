import json
import requests
from pathlib import Path
BASE = Path(__file__).resolve().parent
TOKEN_PATH = BASE / "storage" / "secrets" / "ebay_access_token.txt"
def get_token():
    return TOKEN_PATH.read_text(encoding="utf-8").strip()
def main():
    offer_id = "REPLACE_WITH_YOUR_OFFER_ID"
    url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}"
    payload = {
        "pricingSummary": {
            "price": {
                "value": "4.99",
                "currency": "EUR"
            }
        },
        "listingPolicies": {
            "fulfillmentPolicyId": "REPLACE",
            "paymentPolicyId": "REPLACE",
            "returnPolicyId": "REPLACE"
        }
    }
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }
    r = requests.put(url, headers=headers, json=payload)
    print("OFFER_UPDATE")
    print("http_status =", r.status_code)
    try:
        print("response =", r.json())
    except:
        print("response_text =", r.text)
if __name__ == "__main__":
    main()
