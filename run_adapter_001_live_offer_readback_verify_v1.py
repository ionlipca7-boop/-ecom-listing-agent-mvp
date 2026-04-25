import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
OFFER_ID = "153365657011"
LIVE_OUT = ROOT / "storage" / "exports" / "adapter_001_live_offer_readback_v1.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_live_offer_readback_audit_v1.json"

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    url = "https://api.ebay.com/sell/inventory/v1/offer/" + OFFER_ID
    resp = requests.get(url, headers=headers, timeout=60)
    try:
        data = resp.json()
    except Exception:
        data = {"raw_text": resp.text}
    LIVE_OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    policies = data.get("listingPolicies", {}) if isinstance(data, dict) else {}
    price_obj = data.get("pricingSummary", {}).get("price", {}) if isinstance(data, dict) else {}
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_live_offer_readback_verify_v1_completed"
    result["offer_id"] = OFFER_ID
    result["read_status"] = resp.status_code
    result["sku"] = data.get("sku", "")
    result["categoryId"] = data.get("categoryId", "")
    result["availableQuantity"] = data.get("availableQuantity", "")
    result["price_value"] = price_obj.get("value", "")
    result["price_currency"] = price_obj.get("currency", "")
    result["merchantLocationKey"] = data.get("merchantLocationKey", "")
    result["listingPolicies"] = policies
    result["policy_keys"] = sorted(list(policies.keys())) if isinstance(policies, dict) else []
    result["next_step"] = "prepare_full_offer_payload_with_real_policy_ids_and_shipping_rules_if_needed"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_LIVE_OFFER_READBACK_VERIFY_V1")
    print("status =", result["status"])
    print("read_status =", result["read_status"])
    print("sku =", result["sku"])
    print("price_value =", result["price_value"])
    print("merchantLocationKey =", result["merchantLocationKey"])
    print("policy_keys =", result["policy_keys"])
if __name__ == "__main__":
    main()
