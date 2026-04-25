import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_POLICIES = EXPORTS_DIR / "ebay_policies_v1.json"
INPUT_PAYLOAD = EXPORTS_DIR / "real_offer_request_payload_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "real_offer_request_payload_v2.json"

def main():
    policies = json.loads(INPUT_POLICIES.read_text(encoding="utf-8"))
    payload_doc = json.loads(INPUT_PAYLOAD.read_text(encoding="utf-8"))
    payload = payload_doc.get("payload", {})
    listing = payload.get("listingPolicies", {})

    fulfillment_id = ((policies.get("fulfillment_policies") or [{}])[0]).get("id", "")
    payment_id = ((policies.get("payment_policies") or [{}])[0]).get("id", "")
    return_id = ((policies.get("return_policies") or [{}])[0]).get("id", "")

    listing["fulfillmentPolicyId"] = fulfillment_id
    listing["paymentPolicyId"] = payment_id
    listing["returnPolicyId"] = return_id
    payload["listingPolicies"] = listing
    payload_doc["payload"] = payload

    missing = []
    if payload.get("categoryId") in ["", "0", None]:
        missing.append("categoryId")
    if not listing.get("fulfillmentPolicyId"):
        missing.append("fulfillmentPolicyId")
    if not listing.get("paymentPolicyId"):
        missing.append("paymentPolicyId")
    if not listing.get("returnPolicyId"):
        missing.append("returnPolicyId")

    result = {
        "status": "OK",
        "decision": "policies_injected_into_payload",
        "selected_policy_ids": {
            "fulfillmentPolicyId": fulfillment_id,
            "paymentPolicyId": payment_id,
            "returnPolicyId": return_id
        },
        "missing_runtime_values": missing,
        "payload": payload
    }

    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SELECT_EBAY_POLICIES_V1")
    print("fulfillmentPolicyId =", fulfillment_id)
    print("paymentPolicyId =", payment_id)
    print("returnPolicyId =", return_id)
    print("missing_runtime_values =", missing)

if __name__ == "__main__":
    main()
