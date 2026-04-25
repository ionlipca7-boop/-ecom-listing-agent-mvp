import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
SKU = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
OFFER_ID = "153365657011"
OFFER_PAYLOAD_OUT = ROOT / "storage" / "exports" / "adapter_001_marker_update_offer_payload_v1.json"
OFFER_RESPONSE_OUT = ROOT / "storage" / "exports" / "adapter_001_marker_update_offer_response_v1.json"
OFFER_READBACK_OUT = ROOT / "storage" / "exports" / "adapter_001_marker_update_offer_readback_v1.json"
INV_READBACK_OUT = ROOT / "storage" / "exports" / "adapter_001_marker_update_inventory_readback_v1.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_marker_update_and_verify_audit_v1.json"
TARGET_PRICE = "4.01"
TARGET_CURRENCY = "EUR"

def get_json(url, headers):
    resp = requests.get(url, headers=headers, timeout=60)
    try:
        data = resp.json()
    except Exception:
        data = {"raw_text": resp.text}
    return resp, data

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    offer_url = "https://api.ebay.com/sell/inventory/v1/offer/" + OFFER_ID
    inv_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + SKU
    offer_get_resp, offer_live = get_json(offer_url, headers)
    payload = {}
    payload["sku"] = offer_live.get("sku", SKU)
    payload["marketplaceId"] = offer_live.get("marketplaceId", "EBAY_DE")
    payload["format"] = offer_live.get("format", "FIXED_PRICE")
    payload["availableQuantity"] = offer_live.get("availableQuantity", 12)
    payload["categoryId"] = offer_live.get("categoryId", "44932")
    payload["merchantLocationKey"] = offer_live.get("merchantLocationKey", "")
    payload["listingPolicies"] = offer_live.get("listingPolicies", {})
    payload["pricingSummary"] = {"price": {"value": TARGET_PRICE, "currency": TARGET_CURRENCY}}
    if "listingDescription" in offer_live:
        payload["listingDescription"] = offer_live.get("listingDescription", "")
    if "quantityLimitPerBuyer" in offer_live:
        payload["quantityLimitPerBuyer"] = offer_live.get("quantityLimitPerBuyer")
    if "tax" in offer_live:
        payload["tax"] = offer_live.get("tax", {})
    OFFER_PAYLOAD_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    offer_put_resp = requests.put(offer_url, headers=headers, json=payload, timeout=60)
    try:
        offer_put_data = offer_put_resp.json()
    except Exception:
        offer_put_data = {"raw_text": offer_put_resp.text}
    OFFER_RESPONSE_OUT.write_text(json.dumps(offer_put_data, indent=2, ensure_ascii=False), encoding="utf-8")
    offer_read_resp, offer_after = get_json(offer_url, headers)
    inv_read_resp, inv_after = get_json(inv_url, headers)
    OFFER_READBACK_OUT.write_text(json.dumps(offer_after, indent=2, ensure_ascii=False), encoding="utf-8")
    INV_READBACK_OUT.write_text(json.dumps(inv_after, indent=2, ensure_ascii=False), encoding="utf-8")
    product = inv_after.get("product", {}) if isinstance(inv_after, dict) else {}
    image_urls = product.get("imageUrls", []) if isinstance(product, dict) else []
    if not isinstance(image_urls, list):
        image_urls = []
    price_obj = offer_after.get("pricingSummary", {}).get("price", {}) if isinstance(offer_after, dict) else {}
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_marker_update_and_verify_v1_completed"
    result["offer_get_status"] = offer_get_resp.status_code
    result["offer_put_status"] = offer_put_resp.status_code
    result["offer_readback_status"] = offer_read_resp.status_code
    result["inventory_readback_status"] = inv_read_resp.status_code
    result["price_value"] = price_obj.get("value", "")
    result["merchantLocationKey"] = offer_after.get("merchantLocationKey", "")
    result["image_count"] = len(image_urls)
    result["listingPolicies"] = offer_after.get("listingPolicies", {})
    result["photo_upgrade_ready"] = "yes" if len(image_urls) == 1 else "already_more_than_one"
    result["next_step"] = "use_real_new_photo_urls_or_uploaded_photos_for_photo_upgrade"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_MARKER_UPDATE_AND_VERIFY_V1")
    print("status =", result["status"])
    print("offer_put_status =", result["offer_put_status"])
    print("offer_readback_status =", result["offer_readback_status"])
    print("inventory_readback_status =", result["inventory_readback_status"])
    print("price_value =", result["price_value"])
    print("merchantLocationKey =", result["merchantLocationKey"])
    print("image_count =", result["image_count"])
if __name__ == "__main__":
    main()
