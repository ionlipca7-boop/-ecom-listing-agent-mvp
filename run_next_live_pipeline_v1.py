import json
import sys
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INVENTORY_FILE = EXPORTS_DIR / "ebay_next_inventory_payload_v1.json"
OFFER_FILE = EXPORTS_DIR / "ebay_next_offer_payload_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "ebay_next_live_pipeline_audit_v1.json"

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {"raw_text": response.text}

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    inventory_payload = json.loads(INVENTORY_FILE.read_text(encoding="utf-8"))
    offer_payload = json.loads(OFFER_FILE.read_text(encoding="utf-8"))
    sku = inventory_payload["sku"]

    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }

    result = {"sku": sku, "steps": {}}

    inventory_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
    r1 = requests.put(inventory_url, headers=headers, json=inventory_payload, timeout=60)
    d1 = safe_json(r1)
    result["steps"]["inventory_upsert"] = {"http_status": r1.status_code, "response_json": d1}
    if r1.status_code != 204:
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("NEXT_LIVE_PIPELINE_V1_FAILED")
        print("failed_step = inventory_upsert")
        print("http_status =", r1.status_code)
        sys.exit(1)

    create_offer_url = "https://api.ebay.com/sell/inventory/v1/offer"
    r2 = requests.post(create_offer_url, headers=headers, json=offer_payload, timeout=60)
    d2 = safe_json(r2)
    result["steps"]["create_offer"] = {"http_status": r2.status_code, "response_json": d2}
    if r2.status_code not in (200, 201):
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("NEXT_LIVE_PIPELINE_V1_FAILED")
        print("failed_step = create_offer")
        print("http_status =", r2.status_code)
        sys.exit(1)

    offer_id = d2.get("offerId")
    result["offerId"] = offer_id

    publish_url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id + "/publish"
    r3 = requests.post(publish_url, headers=headers, timeout=60)
    d3 = safe_json(r3)
    result["steps"]["publish_offer"] = {"http_status": r3.status_code, "response_json": d3}
    result["listingId"] = d3.get("listingId") if isinstance(d3, dict) else None
    result["status"] = "OK" if r3.status_code == 200 else "FAILED"

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if r3.status_code == 200:
        print("NEXT_LIVE_PIPELINE_V1_OK")
        print("sku =", sku)
        print("offerId =", offer_id)
        print("listingId =", result.get("listingId"))
        return

    print("NEXT_LIVE_PIPELINE_V1_FAILED")
    print("failed_step = publish_offer")
    print("http_status =", r3.status_code)
    if isinstance(d3, dict) and d3.get("errors"):
        print("first_error =", d3["errors"][0])
    sys.exit(1)

if __name__ == "__main__":
    main()
