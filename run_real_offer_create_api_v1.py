import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
INPUT_PATH = EXPORTS_DIR / "ebay_draft_with_offer_v1.json"
GATE_PATH = EXPORTS_DIR / "real_api_publish_gate_v1.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"
OUTPUT_PATH = EXPORTS_DIR / "real_offer_create_api_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def safe_load(path):
    if not path.exists():
        return {}
    return load_json(path)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    draft = safe_load(INPUT_PATH)
    gate = safe_load(GATE_PATH)
    token_exists = TOKEN_PATH.exists()
    token_length = int("0")
    if token_exists:
        token_length = len(TOKEN_PATH.read_text(encoding="utf-8").strip())

    title = draft.get("title")
    sku = draft.get("sku")
    price = draft.get("price")
    currency = draft.get("currency")
    quantity = draft.get("quantity")
    placeholder_offer_id = draft.get("offerId")
    format_name = draft.get("format")
    category_hint = draft.get("category_hint")

    missing_fields = []
    if not title:
        missing_fields.append("title")
    if not sku:
        missing_fields.append("sku")
    if price is None:
        missing_fields.append("price")
    if not currency:
        missing_fields.append("currency")
    if quantity is None:
        missing_fields.append("quantity")
    if not format_name:
        missing_fields.append("format")
    if not category_hint:
        missing_fields.append("category_hint")

    required_api_fields = []
    required_api_fields.append("marketplaceId")
    required_api_fields.append("merchantLocationKey")
    required_api_fields.append("listingPolicies")
    required_api_fields.append("inventory_item_ready")

    can_build_real_offer_request = False
    if token_exists:
        if token_length > int("20"):
            if len(missing_fields) == int("0"):
                can_build_real_offer_request = True

    result = {}
    result["status"] = "OK"
    result["source_gate_decision"] = gate.get("decision")
    result["token_exists"] = token_exists
    result["token_length"] = token_length
    result["title"] = title
    result["sku"] = sku
    result["price"] = price
    result["currency"] = currency
    result["quantity"] = quantity
    result["placeholder_offerId"] = placeholder_offer_id
    result["missing_fields"] = missing_fields
    result["required_api_fields"] = required_api_fields
    result["can_build_real_offer_request"] = can_build_real_offer_request
    result["decision"] = "prepare_real_inventory_item_layer"
    result["next_step"] = "run_real_inventory_item_prepare_v1"
    if can_build_real_offer_request:
        result["decision"] = "real_offer_request_payload_next"
        result["next_step"] = "run_real_offer_request_payload_v1"
    save_json(OUTPUT_PATH, result)
    print("REAL_OFFER_CREATE_API_V1_DONE")
    print("status =", result["status"])
    print("token_exists =", result["token_exists"])
    print("can_build_real_offer_request =", result["can_build_real_offer_request"])
    print("decision =", result["decision"])
    print("next_step =", result["next_step"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
