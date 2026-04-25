import json
from datetime import UTC, datetime
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
INPUT_FILE = EXPORTS_DIR / "new_product_adapter_001.json"
PREV_AUDIT_FILE = EXPORTS_DIR / "full_publish_pipeline_v2_audit.json"
OUT_FILE = EXPORTS_DIR / "publish_existing_offer_repair_v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def read_text(path):
    return path.read_text(encoding="utf-8").strip()

def ensure_list(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]

def normalize_aspects(raw_aspects):
    result = {}
    if isinstance(raw_aspects, dict):
        for k, v in raw_aspects.items():
            key = str(k).strip()
            vals = ensure_list(v)
            if key and vals:
                result[key] = vals
    return result

def main():
    product = read_json(INPUT_FILE)
    prev = read_json(PREV_AUDIT_FILE)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    sku = prev.get("sku")
    offer_id = prev.get("offerId")
    title = product.get("title") or product.get("main_title") or "USB-C OTG Adapter USB 3.0 Typ-C auf USB-A"
    description = product.get("description") or title
    aspects = normalize_aspects(product.get("aspects"))
    if "Produktart" not in aspects:
        aspects["Produktart"] = ["Adapter"]
    if "Marke" not in aspects and product.get("brand"):
        aspects["Marke"] = [str(product.get("brand")).strip()]
    if "Herstellernummer" not in aspects:
        aspects["Herstellernummer"] = [str(product.get("mpn") or "Nicht zutreffend").strip()]
    image_urls = ensure_list(product.get("imageUrls") or product.get("image_urls"))
    inventory_payload = {
        "availability": {"shipToLocationAvailability": {"quantity": int(product.get("quantity", 10))}},
        "condition": "NEW",
        "product": {
            "title": title,
            "description": description,
            "aspects": aspects
        }
    }
    if image_urls:
        inventory_payload["product"]["imageUrls"] = image_urls
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Content-Language": "de-DE"}
    result = {
        "status": "OK",
        "decision": "repair_started",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "sku": sku,
        "offerId": offer_id,
        "repair_inventory_payload": inventory_payload,
        "repair_inventory_http_status": None,
        "publish_http_status": None,
        "listingId": None
    }
    inv_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    inv_response = requests.put(inv_url, headers=headers, json=inventory_payload, timeout=60)
    result["repair_inventory_http_status"] = inv_response.status_code
    try:
        result["repair_inventory_response"] = inv_response.json()
    except Exception:
        result["repair_inventory_response_text"] = inv_response.text
    if inv_response.status_code not in (200, 201, 204):
        result["status"] = "ERROR"
        result["decision"] = "repair_inventory_failed"
        OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("PUBLISH_EXISTING_REPAIR_DONE")
        print("status =", result["status"])
        print("decision =", result["decision"])
        print("repair_inventory_http_status =", result["repair_inventory_http_status"])
        return
    publish_url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/publish/"
    publish_response = requests.post(publish_url, headers=headers, timeout=60)
    result["publish_http_status"] = publish_response.status_code
    try:
        publish_raw = publish_response.json()
    except Exception:
        publish_raw = {"raw_text": publish_response.text}
    result["publish_response"] = publish_raw
    if isinstance(publish_raw, dict):
        result["listingId"] = publish_raw.get("listingId") or publish_raw.get("listing_id")
    if publish_response.status_code in (200, 201) and result["listingId"]:
        result["decision"] = "publish_existing_offer_live_ok"
    else:
        result["status"] = "ERROR"
        result["decision"] = "publish_existing_offer_failed"
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PUBLISH_EXISTING_REPAIR_DONE")
    print("status =", result["status"])
    print("decision =", result["decision"])
    print("repair_inventory_http_status =", result["repair_inventory_http_status"])
    print("publish_http_status =", result["publish_http_status"])
    print("listingId =", result["listingId"])

if __name__ == "__main__":
    main()
