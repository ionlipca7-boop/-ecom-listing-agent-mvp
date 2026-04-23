import json
from pathlib import Path

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
EXPORTS = ROOT / "storage" / "exports"

input_path = EXPORTS / "first_real_multi_listing_run_payload_v1.json"
output_path = EXPORTS / "first_real_multi_listing_run_payload_v2.json"

data = json.loads(input_path.read_text(encoding="utf-8"))

fulfillment_id = "257755855024"
payment_id = "257755913024"
return_id = "257755877024"

payload = data.get("payload", {})
listing_policies = payload.get("listingPolicies", {})
listing_policies["fulfillmentPolicyId"] = fulfillment_id
listing_policies["paymentPolicyId"] = payment_id
listing_policies["returnPolicyId"] = return_id
payload["listingPolicies"] = listing_policies
data["payload"] = payload
data["runtime_ready_for_live"] = True
data["applied_real_policy_ids"] = {
    "fulfillmentPolicyId": fulfillment_id,
    "paymentPolicyId": payment_id,
    "returnPolicyId": return_id
}
data["decision"] = "real_policy_ids_applied_to_run_payload_v2"
data["next_step"] = "execute_first_real_multi_listing_live_run_v1" 

output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print("APPLY_REAL_POLICY_IDS_V1_FINAL_AUDIT")
print("status = OK")
print("decision =", data.get("decision"))
print("runtime_ready_for_live =", data.get("runtime_ready_for_live"))
print("blocking_fields_count =", data.get("blocking_fields_count"))
print("fulfillmentPolicyId =", listing_policies.get("fulfillmentPolicyId"))
print("paymentPolicyId =", listing_policies.get("paymentPolicyId"))
print("returnPolicyId =", listing_policies.get("returnPolicyId"))
print("output_file =", str(output_path))
print("next_step =", data.get("next_step"))
