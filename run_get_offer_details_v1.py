import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
PREV_AUDIT_FILE = BASE_DIR / "storage" / "exports" / "publish_existing_offer_repair_v1.json"
OUT_FILE = BASE_DIR / "storage" / "exports" / "offer_details_v1.json"

def main():
    prev = json.loads(PREV_AUDIT_FILE.read_text(encoding="utf-8"))
    offer_id = prev.get("offerId")
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Content-Language": "de-DE"}
    url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}"
    response = requests.get(url, headers=headers, timeout=60)
    result = {"status": "OK", "decision": "offer_details_fetched", "offerId": offer_id, "http_status": response.status_code}
    try:
        result["response"] = response.json()
    except Exception:
        result["response_text"] = response.text
    if response.status_code != 200:
        result["status"] = "ERROR"
        result["decision"] = "offer_details_failed"
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("GET_OFFER_DETAILS_DONE")
    print("status =", result["status"])
    print("decision =", result["decision"])
    print("offerId =", result["offerId"])
    print("http_status =", result["http_status"])

if __name__ == "__main__":
    main()
