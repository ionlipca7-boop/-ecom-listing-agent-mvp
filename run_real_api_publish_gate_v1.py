import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
PIPELINE_PATH = EXPORTS_DIR / "listing_pipeline_status_v2.json"
DRAFT_WITH_OFFER_PATH = EXPORTS_DIR / "ebay_draft_with_offer_v1.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"
OUTPUT_PATH = EXPORTS_DIR / "real_api_publish_gate_v1.json"

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
    pipeline = safe_load(PIPELINE_PATH)
    draft = safe_load(DRAFT_WITH_OFFER_PATH)
    offer_id = draft.get("offerId")
    sku = draft.get("sku")
    token_exists = TOKEN_PATH.exists()
    token_text = ""
    if token_exists:
        token_text = TOKEN_PATH.read_text(encoding="utf-8").strip()
    token_length = len(token_text)
    has_real_offer = False
    if offer_id:
        if not str(offer_id).startswith("DRAFT-"):
            has_real_offer = True
    ready = False
    if token_exists:
        if token_length > int("20"):
            if has_real_offer:
                if sku:
                    ready = True
    result = {}
    result["status"] = "OK"
    result["pipeline_status"] = pipeline.get("pipeline_status")
    result["mode"] = pipeline.get("mode")
    result["offerId"] = offer_id
    result["sku"] = sku
    result["token_exists"] = token_exists
    result["token_length"] = token_length
    result["has_real_offer"] = has_real_offer
    result["ready_for_real_api_publish"] = ready
    result["decision"] = "build_real_offer_api_layer"
    result["next_step"] = "run_real_offer_create_api_v1"
    if ready:
        result["decision"] = "real_api_publish_ready"
        result["next_step"] = "run_real_api_publish_v1"
    save_json(OUTPUT_PATH, result)
    print("REAL_API_PUBLISH_GATE_V1_DONE")
    print("status =", result["status"])
    print("has_real_offer =", result["has_real_offer"])
    print("token_exists =", result["token_exists"])
    print("ready_for_real_api_publish =", result["ready_for_real_api_publish"])
    print("next_step =", result["next_step"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
