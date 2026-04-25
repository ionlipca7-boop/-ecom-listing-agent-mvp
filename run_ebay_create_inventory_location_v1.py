import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def read_secret(name):
    return (SECRETS_DIR / name).read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_secret("ebay_access_token.txt")
    merchant_location_key = "ECOM_DE_LOC_1"
    payload = {
        "location": {
            "address": {
                "addressLine1": "Musterstrasse 1",
                "city": "Berlin",
                "postalCode": "10115",
                "country": "DE"
            }
        },
        "name": "ECOM DE MAIN LOCATION",
        "merchantLocationStatus": "ENABLED",
        "locationTypes": ["WAREHOUSE"]
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.ebay.com/sell/inventory/v1/location/" + merchant_location_key,
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Content-Language": "de-DE"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.getcode()
            raw = resp.read().decode("utf-8")
        data = json.loads(raw) if raw else {}
        audit = {
            "status": "OK",
            "http_status": status_code,
            "merchantLocationKey": merchant_location_key,
            "body": data
        }
        (EXPORTS_DIR / "ebay_create_inventory_location_v1.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (EXPORTS_DIR / "ebay_create_inventory_location_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CREATE_INVENTORY_LOCATION_OK")
        print("http_status =", status_code)
        print("merchantLocationKey =", merchant_location_key)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        audit = {
            "status": "FAILED",
            "http_status": e.code,
            "merchantLocationKey": merchant_location_key,
            "request_payload": payload,
            "body": raw
        }
        (EXPORTS_DIR / "ebay_create_inventory_location_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CREATE_INVENTORY_LOCATION_FAILED")
        print("http_status =", e.code)
        print(raw)

if __name__ == "__main__":
    main()
