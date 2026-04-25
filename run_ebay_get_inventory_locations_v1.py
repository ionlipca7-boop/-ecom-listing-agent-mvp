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

    req = urllib.request.Request(
        "https://api.ebay.com/sell/inventory/v1/location",
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Content-Language": "de-DE"
        },
        method="GET"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.getcode()
            raw = resp.read().decode("utf-8")
        data = json.loads(raw) if raw else {}
        locations = data.get("locations", [])
        audit = {
            "status": "OK",
            "http_status": status_code,
            "location_count": len(locations),
            "merchantLocationKeys": [x.get("merchantLocationKey") for x in locations]
        }
        (EXPORTS_DIR / "ebay_inventory_locations_v1.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (EXPORTS_DIR / "ebay_inventory_locations_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("GET_INVENTORY_LOCATIONS_OK")
        print("http_status =", status_code)
        print("location_count =", len(locations))
        if locations:
            print("merchantLocationKey =", locations[0].get("merchantLocationKey"))
        else:
            print("merchantLocationKey = NONE")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        audit = {
            "status": "FAILED",
            "http_status": e.code,
            "body": raw
        }
        (EXPORTS_DIR / "ebay_inventory_locations_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("GET_INVENTORY_LOCATIONS_FAILED")
        print("http_status =", e.code)
        print(raw)

if __name__ == "__main__":
    main()
