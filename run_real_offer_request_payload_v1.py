import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "real_offer_create_api_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "real_offer_request_payload_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    if not INPUT_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "real offer create api file not found"
        save_json(OUTPUT_PATH, result)
        print("REAL_OFFER_REQUEST_PAYLOAD_V1_ERROR")
        print("reason =", result["reason"])
        return

    data = load_json(INPUT_PATH)
    sku = data.get("sku")
    price = data.get("price")
    currency = data.get("currency")
    quantity = data.get("quantity")

    payload = {}
    payload["sku"] = sku
    payload["marketplaceId"] = "EBAY_DE"
    payload["format"] = "FIXED_PRICE"
    payload["availableQuantity"] = quantity
    payload["categoryId"] = "0"
    payload["merchantLocationKey"] = "DEFAULT"
    payload["pricingSummary"] = {}
    payload["pricingSummary"]["price"] = {}
    payload["pricingSummary"]["price"]["value"] = str(price)
    payload["pricingSummary"]["price"]["currency"] = currency
    payload["listingPolicies"] = {}
    payload["listingPolicies"]["fulfillmentPolicyId"] = "REPLACE_ME"
    payload["listingPolicies"]["paymentPolicyId"] = "REPLACE_ME"
    payload["listingPolicies"]["returnPolicyId"] = "REPLACE_ME"

    result = {}
    result["status"] = "OK"
    result["decision"] = "real_offer_payload_prepared"
    result["sku"] = sku
    result["payload"] = payload
    result["missing_runtime_values"] = []
    result["missing_runtime_values"].append("real_categoryId")
    result["missing_runtime_values"].append("merchantLocationKey")
    result["missing_runtime_values"].append("fulfillmentPolicyId")
    result["missing_runtime_values"].append("paymentPolicyId")
    result["missing_runtime_values"].append("returnPolicyId")
    result["next_step"] = "run_real_offer_payload_gate_v1"
    save_json(OUTPUT_PATH, result)
    print("REAL_OFFER_REQUEST_PAYLOAD_V1_DONE")
    print("status =", result["status"])
    print("decision =", result["decision"])
    print("sku =", result["sku"])
    print("next_step =", result["next_step"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
