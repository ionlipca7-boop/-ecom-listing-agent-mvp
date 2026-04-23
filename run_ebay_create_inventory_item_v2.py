import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def read_secret(name):
    return (SECRETS_DIR / name).read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_secret("ebay_access_token.txt")
    sku = "ECOM-TEST-CABLE-001"
    payload = {
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 10
            }
        },
        "condition": "NEW"
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.ebay.com/sell/inventory/v1/inventory_item/" + urllib.parse.quote(sku),
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Content-Language": "de-DE"
        },
        method="PUT"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.getcode()
            raw = resp.read().decode("utf-8")
        data = json.loads(raw) if raw else {}
        audit = {
            "status": "OK",
            "http_status": status_code,
            "sku": sku,
            "request_payload": payload,
            "body": data
        }
        (EXPORTS_DIR / "ebay_create_inventory_item_v2.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (EXPORTS_DIR / "ebay_create_inventory_item_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CREATE_INVENTORY_ITEM_V2_OK")
        print("http_status =", status_code)
        print("sku =", sku)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        audit = {
            "status": "FAILED",
            "http_status": e.code,
            "sku": sku,
            "request_payload": payload,
            "body": raw
        }
        (EXPORTS_DIR / "ebay_create_inventory_item_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CREATE_INVENTORY_ITEM_V2_FAILED")
        print("http_status =", e.code)
        print(raw)

if __name__ == "__main__":
    main()
