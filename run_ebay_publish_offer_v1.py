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
    offer_id = "152921341011"
    req = urllib.request.Request(
        "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id + "/publish",
        data=b"",
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
            "offerId": offer_id,
            "listingId": data.get("listingId"),
            "inventoryItemGroupKey": data.get("inventoryItemGroupKey"),
            "warnings": data.get("warnings"),
            "body": data
        }
        (EXPORTS_DIR / "ebay_publish_offer_v1.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (EXPORTS_DIR / "ebay_publish_offer_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PUBLISH_OFFER_V1_OK")
        print("http_status =", status_code)
        print("offerId =", offer_id)
        print("listingId =", data.get("listingId"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        audit = {
            "status": "FAILED",
            "http_status": e.code,
            "offerId": offer_id,
            "body": raw
        }
        (EXPORTS_DIR / "ebay_publish_offer_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PUBLISH_OFFER_V1_FAILED")
        print("http_status =", e.code)
        print(raw)

if __name__ == "__main__":
    main()
