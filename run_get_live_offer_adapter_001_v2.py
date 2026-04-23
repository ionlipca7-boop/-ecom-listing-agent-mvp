import json
from pathlib import Path
import requests
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
SECRET_DIR = BASE_DIR / "storage" / "secrets"
def read_text(path):
    return path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
def main():
    offer_id = "153365657011"
    token = read_text(SECRET_DIR / "ebay_access_token.txt")
    url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Language": "de-DE"}
    response = requests.get(url, headers=headers, timeout=60)
    data = response.json() if response.text.strip() else {}
    out_path = EXPORT_DIR / "adapter_001_live_offer_v2.json"
    audit_path = EXPORT_DIR / "adapter_001_live_offer_audit_v2.json"
    if response.status_code == 200:
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {"status": "OK" if response.status_code == 200 else "ERROR", "decision": "adapter_001_live_offer_v2_fetched" if response.status_code == 200 else "adapter_001_live_offer_v2_fetch_failed", "http_status": response.status_code, "offerId": offer_id, "sku": data.get("sku"), "availableQuantity": data.get("availableQuantity"), "has_price": bool(data.get("pricingSummary", {}).get("price")), "has_policies": bool(data.get("listingPolicies"))}
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_LIVE_OFFER_V2_FETCH_DONE")
    print("http_status =", response.status_code)
    print("audit_file =", str(audit_path))
if __name__ == "__main__":
    main()
