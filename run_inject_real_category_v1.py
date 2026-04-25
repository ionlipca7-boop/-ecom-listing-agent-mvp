import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PAYLOAD = EXPORTS_DIR / "real_offer_request_payload_v2.json"
INPUT_CATEGORY = EXPORTS_DIR / "real_category_select_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "real_offer_request_payload_v3.json"

def main():
    payload_doc = json.loads(INPUT_PAYLOAD.read_text(encoding="utf-8"))
    category_doc = json.loads(INPUT_CATEGORY.read_text(encoding="utf-8"))
    payload = payload_doc.get("payload", {})
    selected = category_doc.get("selected_category", {})
    category_id = selected.get("categoryId", "")
    category_name = selected.get("categoryName", "")
    payload["categoryId"] = category_id
    missing = []
    if not payload.get("categoryId"):
        missing.append("categoryId")
    if not payload.get("merchantLocationKey"):
        missing.append("merchantLocationKey")
    listing = payload.get("listingPolicies", {})
    if not listing.get("fulfillmentPolicyId"):
        missing.append("fulfillmentPolicyId")
    if not listing.get("paymentPolicyId"):
        missing.append("paymentPolicyId")
    if not listing.get("returnPolicyId"):
        missing.append("returnPolicyId")
    result = {
        "status": "OK",
        "decision": "real_category_injected",
        "selected_category": {
            "categoryId": category_id,
            "categoryName": category_name
        },
        "missing_runtime_values": missing,
        "payload": payload
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("INJECT_REAL_CATEGORY_V1")
    print("categoryId =", category_id)
    print("categoryName =", category_name)
    print("missing_runtime_values =", missing)

if __name__ == "__main__":
    main()
