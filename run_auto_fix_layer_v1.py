import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "auto_fix_layer_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    feedback_layer = read_json(EXPORTS_DIR / "feedback_status_layer_v1.json")
    parsed_data = read_json(EXPORTS_DIR / "ebay_upload_result_parsed_v1.json")

    items = parsed_data.get("items", [])
    success_count = feedback_layer.get("success_count", 0)
    warning_count = feedback_layer.get("warning_count", 0)
    error_count = feedback_layer.get("error_count", 0)
    unknown_count = feedback_layer.get("unknown_count", 0)
    feedback_status = feedback_layer.get("feedback_layer_status", "")

    recommended_action = "NO_FIX_NEEDED"
    auto_fix_status = "READY"
    next_step = "BUILD_OPTIMIZATION_STATUS_LAYER"
    fix_reason = "Upload feedback is clean"

    if feedback_status != "READY":
        recommended_action = "WAIT_FOR_VALID_FEEDBACK"
        auto_fix_status = "BLOCKED"
        next_step = "FIX_FEEDBACK_LAYER"
        fix_reason = "Feedback layer is not ready"
    elif error_count > 0:
        recommended_action = "BUILD_ERROR_FIX_MAP"
        auto_fix_status = "ATTENTION"
        next_step = "MAP_ERRORS_TO_FIXES"
        fix_reason = "Upload errors detected"
    elif warning_count > 0:
        recommended_action = "REVIEW_WARNINGS"
        auto_fix_status = "ATTENTION"
        next_step = "BUILD_WARNING_REVIEW_LAYER"
        fix_reason = "Upload warnings detected"
    elif unknown_count > 0:
        recommended_action = "REVIEW_UNKNOWN_RESULTS"
        auto_fix_status = "ATTENTION"
        next_step = "BUILD_UNKNOWN_RESULT_REVIEW_LAYER"
        fix_reason = "Unknown upload results detected"

    latest_item_status = ""
    latest_listing_id = ""
    latest_sku = ""

    if items:
        first_item = items[0]
        latest_item_status = first_item.get("status", "")
        raw = first_item.get("raw", {})
        latest_listing_id = raw.get("listing_id", "")
        latest_sku = raw.get("sku", "")

    result = {
        "checked_at": utc_now(),
        "auto_fix_status": auto_fix_status,
        "next_step": next_step,
        "recommended_action": recommended_action,
        "fix_reason": fix_reason,
        "feedback_layer_status": feedback_status,
        "success_count": success_count,
        "warning_count": warning_count,
        "error_count": error_count,
        "unknown_count": unknown_count,
        "latest_item_status": latest_item_status,
        "latest_listing_id": latest_listing_id,
        "latest_sku": latest_sku
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("AUTO_FIX_LAYER_V1:")
    print("auto_fix_status:", result["auto_fix_status"])
    print("next_step:", result["next_step"])
    print("recommended_action:", result["recommended_action"])
    print("fix_reason:", result["fix_reason"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
