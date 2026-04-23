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
    upgrade_path = EXPORT_DIR / "adapter_001_specifics_upgrade_v1.json"
    token_path = SECRET_DIR / "ebay_access_token.txt"
    if not upgrade_path.exists():
        raise FileNotFoundError("Missing upgrade file: " + str(upgrade_path))
    if not token_path.exists():
        raise FileNotFoundError("Missing token file: " + str(token_path))
    upgrade = read_json(upgrade_path)
    token = read_text(token_path)
    sku = upgrade["sku"]
    specifics = upgrade["recommended_item_specifics"]
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Content-Language": "de-DE",
        "Accept": "application/json" 
    }
    payload = {
        "sku": sku,
        "product": {
            "aspects": specifics
        }
    }
    response = requests.put(url, headers=headers, json=payload, timeout=60)
    raw_text = response.text
    try:
        response_json = response.json() if raw_text.strip() else {}
    except Exception:
        response_json = {"raw_text": raw_text}
    audit = {
        "status": "OK" if response.status_code in (200, 204) else "ERROR",
        "decision": "adapter_001_live_specifics_revised" if response.status_code in (200, 204) else "adapter_001_live_specifics_revise_failed",
        "http_status": response.status_code,
        "product_key": "adapter_001",
        "sku": sku,
        "offerId": upgrade.get("offerId"),
        "listingId": upgrade.get("listingId"),
        "sent_specifics_count": len(specifics),
        "request_payload": payload,
        "response_body": response_json
    }
    out_path = EXPORT_DIR / "adapter_001_live_specifics_revise_audit_v1.json"
    out_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    if response.status_code in (200, 204):
        print("ADAPTER_001_LIVE_SPECIFICS_REVISE_OK")
    else:
        print("ADAPTER_001_LIVE_SPECIFICS_REVISE_FAILED")
    print("http_status =", response.status_code)
    print("sku =", sku)
    print("sent_specifics_count =", len(specifics))
    print("audit_file =", str(out_path))
if __name__ == "__main__":
    main()
