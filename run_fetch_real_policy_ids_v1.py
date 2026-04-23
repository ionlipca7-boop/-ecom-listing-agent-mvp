import json
import requests
from pathlib import Path

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
SECRETS = ROOT / "storage" / "secrets"
EXPORTS = ROOT / "storage" / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)

token_path = SECRETS / "ebay_access_token.txt"
out_path = EXPORTS / "real_policy_ids_v1.json"
result = {}

if not token_path.exists():
    result["status"] = "ERROR"
    result["decision"] = "missing_access_token_file"
else:
    access_token = token_path.read_text(encoding="utf-8").strip()
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
        "Content-Language": "de-DE" 
    }
    marketplace = "EBAY_DE"
    fulfillment_url = "https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id=" + marketplace
    payment_url = "https://api.ebay.com/sell/account/v1/payment_policy?marketplace_id=" + marketplace
    return_url = "https://api.ebay.com/sell/account/v1/return_policy?marketplace_id=" + marketplace

    r1 = requests.get(fulfillment_url, headers=headers, timeout=60)
    r2 = requests.get(payment_url, headers=headers, timeout=60)
    r3 = requests.get(return_url, headers=headers, timeout=60)

    try:
        j1 = r1.json()
    except Exception:
        j1 = {"raw_text": r1.text}
    try:
        j2 = r2.json()
    except Exception:
        j2 = {"raw_text": r2.text}
    try:
        j3 = r3.json()
    except Exception:
        j3 = {"raw_text": r3.text}

    fulfillment_list = j1.get("fulfillmentPolicies", []) if isinstance(j1, dict) else []
    payment_list = j2.get("paymentPolicies", []) if isinstance(j2, dict) else []
    return_list = j3.get("returnPolicies", []) if isinstance(j3, dict) else []

    result["status"] = "OK" if r1.status_code == 200 and r2.status_code == 200 and r3.status_code == 200 else "ERROR"
    result["decision"] = "real_policy_ids_v1_fetched"
    result["marketplace"] = marketplace
    result["fulfillment_http_status"] = r1.status_code
    result["payment_http_status"] = r2.status_code
    result["return_http_status"] = r3.status_code
    result["fulfillment_count"] = len(fulfillment_list)
    result["payment_count"] = len(payment_list)
    result["return_count"] = len(return_list)
    result["first_fulfillment_policy_id"] = fulfillment_list[0].get("fulfillmentPolicyId") if fulfillment_list else None
    result["first_payment_policy_id"] = payment_list[0].get("paymentPolicyId") if payment_list else None
    result["first_return_policy_id"] = return_list[0].get("returnPolicyId") if return_list else None
    result["fulfillment_policies"] = fulfillment_list
    result["payment_policies"] = payment_list
    result["return_policies"] = return_list

out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("REAL_POLICY_IDS_V1_FINAL_AUDIT")
print("status =", result.get("status"))
print("decision =", result.get("decision"))
print("fulfillment_http_status =", result.get("fulfillment_http_status", "-"))
print("payment_http_status =", result.get("payment_http_status", "-"))
print("return_http_status =", result.get("return_http_status", "-"))
print("fulfillment_count =", result.get("fulfillment_count", 0))
print("payment_count =", result.get("payment_count", 0))
print("return_count =", result.get("return_count", 0))
print("first_fulfillment_policy_id =", result.get("first_fulfillment_policy_id", None))
print("first_payment_policy_id =", result.get("first_payment_policy_id", None))
print("first_return_policy_id =", result.get("first_return_policy_id", None))
print("next_step = map_real_policy_ids_into_live_run_payload")
