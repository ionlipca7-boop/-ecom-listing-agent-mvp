import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
SKU = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
OFFER_ID = "153365657011"
OUT = ROOT / "storage" / "exports" / "adapter_001_approval_package_v1.json"
AUDIT = ROOT / "storage" / "memory" / "archive" / "adapter_001_approval_package_audit_v1.json"

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
    inv_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + SKU
    offer_url = "https://api.ebay.com/sell/inventory/v1/offer/" + OFFER_ID
    inv_resp, inv_data = get_json(inv_url, headers)
    offer_resp, offer_data = get_json(offer_url, headers)
    product = inv_data.get("product", {}) if isinstance(inv_data, dict) else {}
    aspects = product.get("aspects", {}) if isinstance(product, dict) else {}
    pws = inv_data.get("packageWeightAndSize", {}) if isinstance(inv_data, dict) else {}
    weight = pws.get("weight", {}) if isinstance(pws, dict) else {}
    dimensions = pws.get("dimensions", {}) if isinstance(pws, dict) else {}
    price_obj = offer_data.get("pricingSummary", {}).get("price", {}) if isinstance(offer_data, dict) else {}
    policies = offer_data.get("listingPolicies", {}) if isinstance(offer_data, dict) else {}
    image_urls = product.get("imageUrls", []) if isinstance(product, dict) else []
    if not isinstance(image_urls, list):
        image_urls = []
    gaps = []
    if len(image_urls) lt 2:
        gaps.append("photo_set_weak")
    if len(aspects) lt 20:
        gaps.append("specifics_can_be_richer")
    if not offer_data.get("listingDescription", ""):
        gaps.append("html_missing")
    package = {}
    package["status"] = "OK"
    package["decision"] = "adapter_001_approval_package_v1_created"
    package["mode"] = "approval_first_preview"
    package["item"] = {"sku": SKU, "offerId": OFFER_ID, "title": product.get("title", ""), "description": product.get("description", ""), "html": offer_data.get("listingDescription", ""), "price_value": price_obj.get("value", ""), "price_currency": price_obj.get("currency", ""), "availableQuantity": offer_data.get("availableQuantity", ""), "merchantLocationKey": offer_data.get("merchantLocationKey", ""), "categoryId": offer_data.get("categoryId", ""), "image_count": len(image_urls), "image_urls": image_urls, "aspect_count": len(aspects), "aspects": aspects, "weight": weight, "dimensions": dimensions, "listingPolicies": policies}
    package["gaps"] = gaps
    package["recommended_next_actions"] = ["photo_upgrade", "shipping_location_display_cleanup", "optional_multi_buy_discount", "optional_ad_review_after_48h"]
    package["approval_options"] = ["approve_current_as_new_base", "improve_photos_next", "improve_shipping_location_next", "rollback_if_user_rejects"]
    OUT.write_text(json.dumps(package, indent=2, ensure_ascii=False), encoding="utf-8")
    audit = {}
    audit["status"] = "OK"
    audit["decision"] = "adapter_001_approval_package_v1_created"
    audit["inventory_read_status"] = inv_resp.status_code
    audit["offer_read_status"] = offer_resp.status_code
    audit["title"] = product.get("title", "")
    audit["image_count"] = len(image_urls)
    audit["aspect_count"] = len(aspects)
    audit["price_value"] = price_obj.get("value", "")
    audit["gaps"] = gaps
    audit["next_step"] = "user_selects_approval_option_instead_of_manual_loop"
    AUDIT.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_APPROVAL_PACKAGE_V1")
    print("status =", audit["status"])
    print("inventory_read_status =", audit["inventory_read_status"])
    print("offer_read_status =", audit["offer_read_status"])
    print("image_count =", audit["image_count"])
    print("aspect_count =", audit["aspect_count"])
    print("gaps =", audit["gaps"])
if __name__ == "__main__":
    main()
