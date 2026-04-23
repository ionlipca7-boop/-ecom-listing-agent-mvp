import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
DRAFT_DIAG_PATH = EXPORTS_DIR / "ebay_draft_diagnose_v1.json"
PUBLISH_CHECK_PATH = EXPORTS_DIR / "check_publish_file_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "offer_creation_gate_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    if not DRAFT_DIAG_PATH.exists():
        result = {}
        result["status"] = "ERROR"
        result["reason"] = "draft diagnose file missing"
        result["next_step"] = "run_ebay_draft_diagnose_v1"
        save_json(OUTPUT_PATH, result)
        print("OFFER_CREATION_GATE_V1_ERROR")
        print("reason =", result["reason"])
        return

    draft_diag = load_json(DRAFT_DIAG_PATH)
    publish_check = load_json(PUBLISH_CHECK_PATH) if PUBLISH_CHECK_PATH.exists() else {}

    has_offer_id = bool(draft_diag.get("has_offerId"))
    has_sku = bool(draft_diag.get("has_sku"))
    publish_file_exists = bool(publish_check.get("publish_file_exists"))

    result = {}
    result["status"] = "OK"
    result["has_offerId"] = has_offer_id
    result["has_sku"] = has_sku
    result["publish_file_exists"] = publish_file_exists
    result["decision"] = "need_offer_creation_layer"
    result["next_step"] = "run_ebay_create_offer_from_draft_v1"

    if has_offer_id and has_sku:
        result["decision"] = "publish_ready"
        result["next_step"] = "run_ebay_publish_draft_v1"

    save_json(OUTPUT_PATH, result)
    print("OFFER_CREATION_GATE_V1_DONE")
    print("status =", result["status"])
    print("decision =", result["decision"])
    print("next_step =", result["next_step"])
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
