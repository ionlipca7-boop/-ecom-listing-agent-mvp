import json
from datetime import UTC, datetime
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_v1.json"
INPUT_FILE = EXPORTS_DIR / "new_product_adapter_001.json"
PIPELINE_AUDIT_FILE = EXPORTS_DIR / "full_publish_pipeline_v1_audit.json"
REGISTRY_FILE = BASE_DIR / "storage" / "registry" / "products_registry_v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def read_text(path):
    return path.read_text(encoding="utf-8").strip()

def ensure_list(value):
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]

def patch_registry(product_key, sku, offer_id, listing_id):
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {"products": []}
    if REGISTRY_FILE.exists():
        data = read_json(REGISTRY_FILE)
        if not isinstance(data, dict):
            data = {"products": []}
    products = data.get("products", [])
    if not isinstance(products, list):
        products = []
    updated = False
    for item in products:
        if item.get("product_key") == product_key:
            item["sku"] = sku
            item["offerId"] = offer_id
            item["listingId"] = listing_id
            item["listing_state"] = "LIVE"
            item["updated_at_utc"] = datetime.now(UTC).isoformat()
            updated = True
    if not updated:
        products.append({"product_key": product_key, "sku": sku, "offerId": offer_id, "listingId": listing_id, "listing_state": "LIVE", "updated_at_utc": datetime.now(UTC).isoformat()})
    data["products"] = products
    REGISTRY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    memory = read_json(MEMORY_FILE)
    product = read_json(INPUT_FILE)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    working = memory.get("working_values", {})
    product_key = product.get("product_key", "adapter_001")
    sku = product.get("sku") or product.get("generated_sku") or product_key
    quantity = int(product.get("quantity", 10))
    title = product.get("title") or product.get("main_title") or "USB-C Netzteil Adapter"
    description = product.get("description") or title
    image_urls = ensure_list(product.get("imageUrls") or product.get("image_urls"))
    aspects = product.get("aspects", {})
    if "Produktart" not in aspects:
        aspects["Produktart"] = [product.get("produktart") or "Ladegerat"]
    inventory_payload = {
        "availability": {"shipToLocationAvailability": {"quantity": quantity}},
        "condition": product.get("condition") or "NEW",
        "product": {
            "title": title,
            "description": description,
            "aspects": aspects,
            "imageUrls": image_urls
        }
    }
    common_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Content-Language": "de-DE"}
    audit = {
        "status": "OK",
        "decision": "pipeline_started",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "product_key": product_key,
        "sku": sku,
        "inventory_http_status": None,
        "offer_http_status": None,
        "publish_http_status": None,
        "offerId": None,
        "listingId": None,
        "inventory_payload": inventory_payload
    }
    inv_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    inv_response = requests.put(inv_url, headers=common_headers, json=inventory_payload, timeout=60)
    audit["inventory_http_status"] = inv_response.status_code
    if inv_response.status_code not in (200, 201, 204):
        audit["status"] = "ERROR"
        audit["decision"] = "inventory_failed"
        try:
            audit["inventory_response"] = inv_response.json()
        except Exception:
            audit["inventory_response_text"] = inv_response.text
        PIPELINE_AUDIT_FILE.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("FULL_PIPELINE_DONE")
        print("status =", audit["status"])
        print("decision =", audit["decision"])
        print("inventory_http_status =", audit["inventory_http_status"])
        return
    price_value = str(product.get("price") or product.get("price_eur") or "19.99")
    offer_payload = {
        "sku": sku,
        "marketplaceId": working.get("marketplaceId", "EBAY_DE"),
        "format": "FIXED_PRICE",
        "availableQuantity": quantity,
        "categoryId": str(product.get("categoryId") or working.get("working_categoryId") or "44932"),
        "merchantLocationKey": working.get("merchantLocationKey", "ECOM_DE_LOC_1"),
        "pricingSummary": {"price": {"value": price_value, "currency": "EUR"}},
        "listingPolicies": {
            "fulfillmentPolicyId": working.get("fulfillmentPolicyId"),
            "paymentPolicyId": working.get("paymentPolicyId"),
            "returnPolicyId": working.get("returnPolicyId")
        }
    }
    offer_response = requests.post("https://api.ebay.com/sell/inventory/v1/offer", headers=common_headers, json=offer_payload, timeout=60)
    audit["offer_http_status"] = offer_response.status_code
    audit["offer_payload"] = offer_payload
    try:
        offer_raw = offer_response.json()
    except Exception:
        offer_raw = {"raw_text": offer_response.text}
    audit["offer_response"] = offer_raw
    offer_id = offer_raw.get("offerId") if isinstance(offer_raw, dict) else None
    audit["offerId"] = offer_id
    if offer_response.status_code not in (200, 201) or not offer_id:
        audit["status"] = "ERROR"
        audit["decision"] = "offer_failed"
        PIPELINE_AUDIT_FILE.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("FULL_PIPELINE_DONE")
        print("status =", audit["status"])
        print("decision =", audit["decision"])
        print("offer_http_status =", audit["offer_http_status"])
        return
    publish_url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/publish/"
    publish_response = requests.post(publish_url, headers=common_headers, timeout=60)
    audit["publish_http_status"] = publish_response.status_code
    try:
        publish_raw = publish_response.json()
    except Exception:
        publish_raw = {"raw_text": publish_response.text}
    audit["publish_response"] = publish_raw
    listing_id = None
    if isinstance(publish_raw, dict):
        listing_id = publish_raw.get("listingId") or publish_raw.get("listing_id")
    audit["listingId"] = listing_id
    if publish_response.status_code not in (200, 201) or not listing_id:
        audit["status"] = "ERROR"
        audit["decision"] = "publish_failed"
        PIPELINE_AUDIT_FILE.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("FULL_PIPELINE_DONE")
        print("status =", audit["status"])
        print("decision =", audit["decision"])
        print("publish_http_status =", audit["publish_http_status"])
        return
    patch_registry(product_key, sku, offer_id, listing_id)
    audit["decision"] = "pipeline_live_ok"
    PIPELINE_AUDIT_FILE.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("FULL_PIPELINE_DONE")
    print("status =", audit["status"])
    print("decision =", audit["decision"])
    print("inventory_http_status =", audit["inventory_http_status"])
    print("offer_http_status =", audit["offer_http_status"])
    print("publish_http_status =", audit["publish_http_status"])
    print("offerId =", audit["offerId"])
    print("listingId =", audit["listingId"])

if __name__ == "__main__":
    main()
