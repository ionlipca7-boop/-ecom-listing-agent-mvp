import json
from datetime import UTC, datetime
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
REGISTRY_FILE = BASE_DIR / "storage" / "registry" / "products_registry_v1.json"
INPUT_FILE = EXPORTS_DIR / "new_product_adapter_001.json"
PREV_FILE = EXPORTS_DIR / "publish_existing_offer_repair_v2.json"
OUT_FILE = EXPORTS_DIR / "publish_existing_offer_repair_v3.json"

IMAGE_URLS = [
    "https://ae01.alicdn.com/kf/S42fabc33d69c4f5592466804c540a072T.jpg",
    "https://ae01.alicdn.com/kf/Sc68f16cdbb0e48ca9f68da607d90f55fO.jpg",
    "https://ae01.alicdn.com/kf/Sceae79ed63dc4d5aab039de4a52879c8r.jpg",
    "https://ae01.alicdn.com/kf/S8893d5727a1446bb860b97548ede5410X.jpg",
    "https://ae01.alicdn.com/kf/S4f8750a0169946e0b4fc1a0f1b23089aB.jpg",
    "https://ae01.alicdn.com/kf/S3a9306f37bbf44d28dcc5d7b5aaa5c7bl.jpg",
    "https://ae01.alicdn.com/kf/Sadcd253f429a49b8a3460fe75febf721R.jpg",
    "https://ae01.alicdn.com/kf/Se63d8168e9664e28b5c0878026e2445an.jpg",
    "https://ae01.alicdn.com/kf/S21d6d1cf19c341c7928d286cd6a6e8957.jpg"
]

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
    product = read_json(INPUT_FILE)
    prev = read_json(PREV_FILE)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    sku = prev.get("sku")
    offer_id = prev.get("offerId")
    product_key = product.get("product_key", "adapter_001")
    title = product.get("title") or product.get("main_title") or "USB-C OTG Adapter USB 3.0 Typ-C auf USB-A Schnellladen Daten"
    description = product.get("description") or title
    raw_aspects = product.get("aspects") if isinstance(product.get("aspects"), dict) else {}
    aspects = {}
    for k, v in raw_aspects.items():
        key = str(k).strip()
        vals = ensure_list(v)
        if key and vals:
            aspects[key] = vals
    aspects["Produktart"] = ensure_list(aspects.get("Produktart") or product.get("produktart") or "USB-C OTG Adapter")
    aspects["Marke"] = ensure_list(product.get("brand") or "No-Name")
    aspects["Herstellernummer"] = ensure_list(product.get("mpn") or "Nicht zutreffend")
    inventory_payload = {
        "availability": {"shipToLocationAvailability": {"quantity": int(product.get("quantity", 10))}},
        "condition": "NEW",
        "product": {
            "title": title,
            "description": description,
            "aspects": aspects,
            "imageUrls": IMAGE_URLS
        }
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Content-Language": "de-DE"}
    result = {
        "status": "OK",
        "decision": "repair_started",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "product_key": product_key,
        "sku": sku,
        "offerId": offer_id,
        "image_count": len(IMAGE_URLS),
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
        print("PUBLISH_EXISTING_REPAIR_V3_DONE")
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
        patch_registry(product_key, sku, offer_id, result["listingId"])
    else:
        result["status"] = "ERROR"
        result["decision"] = "publish_existing_offer_failed"
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PUBLISH_EXISTING_REPAIR_V3_DONE")
    print("status =", result["status"])
    print("decision =", result["decision"])
    print("image_count =", result["image_count"])
    print("repair_inventory_http_status =", result["repair_inventory_http_status"])
    print("publish_http_status =", result["publish_http_status"])
    print("listingId =", result["listingId"])

if __name__ == "__main__":
    main()
