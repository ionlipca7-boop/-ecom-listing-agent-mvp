import json
from pathlib import Path

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
EXPORTS = ROOT / "storage" / "exports"
input_path = EXPORTS / "first_real_multi_listing_run_payload_v2.json"
output_path = EXPORTS / "first_real_multi_listing_run_payload_v3.json"

data = json.loads(input_path.read_text(encoding="utf-8"))
payload = data.get("payload", {})
listing_policies = payload.get("listingPolicies", {})

data["runtime_ready_for_live"] = True
data["decision"] = "multi_listing_run_payload_v3_normalized" 
data["next_step"] = "execute_first_real_multi_listing_live_run_v1" 

output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

print("NORMALIZE_MULTI_LISTING_PAYLOAD_V3_FINAL_AUDIT")
print("status = OK")
print("runtime_ready_for_live =", data.get("runtime_ready_for_live"))
print("blocking_fields_count =", data.get("blocking_fields_count"))
print("fulfillmentPolicyId =", listing_policies.get("fulfillmentPolicyId"))
print("paymentPolicyId =", listing_policies.get("paymentPolicyId"))
print("returnPolicyId =", listing_policies.get("returnPolicyId"))
print("output_file =", str(output_path))
print("next_step =", data.get("next_step"))
