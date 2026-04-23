import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORT_PATH = BASE_DIR / "storage" / "exports" / "real_offer_request_payload_v1.json"
OUTPUT_PATH = BASE_DIR / "storage" / "exports" / "real_offer_payload_gate_v1.json"

def main():
    data = json.loads(EXPORT_PATH.read_text(encoding="utf-8"))
    payload = data.get("payload", {})
    policies = payload.get("listingPolicies", {})
    missing = []

    if payload.get("categoryId") in ["0", "", None]:
        missing.append("categoryId")
    if not payload.get("merchantLocationKey"):
        missing.append("merchantLocationKey")
    if not policies.get("fulfillmentPolicyId") or policies.get("fulfillmentPolicyId") == "REPLACE_ME":
        missing.append("fulfillmentPolicyId")
    if not policies.get("paymentPolicyId") or policies.get("paymentPolicyId") == "REPLACE_ME":
        missing.append("paymentPolicyId")
    if not policies.get("returnPolicyId") or policies.get("returnPolicyId") == "REPLACE_ME":
        missing.append("returnPolicyId")

    is_ready = not missing
    decision = "ready_for_real_api" if is_ready else "missing_required_fields"
    result = {
        "status": "OK",
        "decision": decision,
        "is_ready": is_ready,
        "missing_fields": missing
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("REAL_OFFER_PAYLOAD_GATE_V1")
    print("is_ready =", is_ready)
    print("missing =", missing)

if __name__ == "__main__":
    main()
