import json
from pathlib import Path
import requests
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
SECRET_DIR = BASE_DIR / "storage" / "secrets"
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def read_text(path):
    return path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
def main():
    update_path = EXPORT_DIR / "adapter_001_full_offer_update_v1.json"
    token_path = SECRET_DIR / "ebay_access_token.txt"
    if not update_path.exists():
        raise FileNotFoundError("Missing file: " + str(update_path))
    if not token_path.exists():
        raise FileNotFoundError("Missing file: " + str(token_path))
    d = read_json(update_path)
    token = read_text(token_path)
    offer_id = d["offerId"]
    payload = d["payload"]
    url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "Content-Language": "de-DE", "Accept": "application/json"}
    response = requests.put(url, headers=headers, json=payload, timeout=60)
    raw_text = response.text
    try:
        response_json = response.json() if raw_text.strip() else {}
    except Exception:
        response_json = {"raw_text": raw_text}
    audit = {
        "status": "OK" if response.status_code in (200, 204) else "ERROR",
        "decision": "adapter_001_live_offer_update_v1_ok" if response.status_code in (200, 204) else "adapter_001_live_offer_update_v1_failed",
        "http_status": response.status_code,
        "offerId": offer_id,
        "sku": payload.get("sku"),
        "new_price": payload.get("pricingSummary", {}).get("price", {}).get("value"),
        "new_quantity": payload.get("availableQuantity"),
        "response_body": response_json
    }
    out_path = EXPORT_DIR / "adapter_001_live_offer_update_audit_v1.json"
    out_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_LIVE_OFFER_UPDATE_V1_DONE")
    print("http_status =", response.status_code)
    print("audit_file =", str(out_path))
if __name__ == "__main__":
    main()
