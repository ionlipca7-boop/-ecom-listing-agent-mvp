import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
LIVE_OFFER_PATH = ROOT / "storage" / "exports" / "adapter_001_live_offer_bridge_read_v1.json"
PAYLOAD_OUT = ROOT / "storage" / "exports" / "adapter_001_live_offer_update_payload_v1.json"
RESPONSE_OUT = ROOT / "storage" / "exports" / "adapter_001_live_offer_update_response_v1.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_live_offer_update_audit_v1.json"
TARGET_PRICE = "3.99"
TARGET_CURRENCY = "EUR"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    live_offer = load_json(LIVE_OFFER_PATH)
    offer_id = live_offer.get("offerId", "")
    payload = {}
    payload["sku"] = live_offer.get("sku", "")
    payload["marketplaceId"] = live_offer.get("marketplaceId", "EBAY_DE")
    payload["format"] = live_offer.get("format", "FIXED_PRICE")
    payload["availableQuantity"] = live_offer.get("availableQuantity", 10)
    payload["categoryId"] = live_offer.get("categoryId", "")
    payload["merchantLocationKey"] = live_offer.get("merchantLocationKey", "")
    payload["listingPolicies"] = live_offer.get("listingPolicies", {})
    pricing = {}
    pricing["price"] = {"value": TARGET_PRICE, "currency": TARGET_CURRENCY}
    payload["pricingSummary"] = pricing
    if "quantityLimitPerBuyer" in live_offer:
        payload["quantityLimitPerBuyer"] = live_offer.get("quantityLimitPerBuyer")
    if "listingDescription" in live_offer:
        payload["listingDescription"] = live_offer.get("listingDescription", "")
    if "tax" in live_offer:
        payload["tax"] = live_offer.get("tax", {})
    url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    PAYLOAD_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    resp = requests.put(url, headers=headers, json=payload, timeout=60)
    try:
        resp_data = resp.json()
    except Exception:
        resp_data = {"raw_text": resp.text}
    RESPONSE_OUT.write_text(json.dumps(resp_data, indent=2, ensure_ascii=False), encoding="utf-8")
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_live_offer_update_v1_completed"
    result["offer_id"] = offer_id
    result["sku"] = payload.get("sku", "")
    result["update_status"] = resp.status_code
    result["price_value"] = payload.get("pricingSummary", {}).get("price", {}).get("value", "")
    result["merchantLocationKey"] = payload.get("merchantLocationKey", "")
    result["policy_keys"] = sorted(list(payload.get("listingPolicies", {}).keys()))
    result["next_step"] = "read_back_offer_after_update_then_prepare_shipping_location_policy_changes_if_needed"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_LIVE_OFFER_UPDATE_V1")
    print("status =", result["status"])
    print("offer_id =", result["offer_id"])
    print("update_status =", result["update_status"])
    print("price_value =", result["price_value"])
    print("merchantLocationKey =", result["merchantLocationKey"])
if __name__ == "__main__":
    main()
