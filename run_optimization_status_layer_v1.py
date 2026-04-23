import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "optimization_status_layer_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    auto_fix_data = read_json(EXPORTS_DIR / "auto_fix_layer_v1.json")
    performance_data = read_json(EXPORTS_DIR / "listing_performance_v1.json")
    price_data = read_json(EXPORTS_DIR / "price_optimizer_v1.json")
    title_data = read_json(EXPORTS_DIR / "ai_title_optimizer_v1.json")
    variant_data = read_json(EXPORTS_DIR / "variant_selector_v1.json")

    auto_fix_status = auto_fix_data.get("auto_fix_status", "")
    recommended_action = auto_fix_data.get("recommended_action", "")
    latest_listing_id = auto_fix_data.get("latest_listing_id", "")
    latest_sku = auto_fix_data.get("latest_sku", "")

    performance_status = performance_data.get("performance_status", "")
    price_status = price_data.get("optimizer_status", "")
    title_status = title_data.get("optimizer_status", "")

    selected_variant = variant_data.get("selected_variant", {})
    selected_title = selected_variant.get("title", "")
    selected_price = selected_variant.get("price", "")
    selected_angle = selected_variant.get("angle", "")

    layer_status = "READY"
    next_step = "BUILD_AI_SYSTEM_LAYER"
    optimization_mode = "POST_UPLOAD_CLEAN_OPTIMIZATION"
    optimization_reason = "Feedback clean, auto-fix not required"

    if auto_fix_status != "READY":
        layer_status = "BLOCKED"
        next_step = "FIX_AUTO_FIX_LAYER"
        optimization_mode = "WAIT"
        optimization_reason = "Auto-fix layer not ready"
    elif recommended_action != "NO_FIX_NEEDED":
        layer_status = "ATTENTION"
        next_step = "REVIEW_AUTO_FIX_DECISION"
        optimization_mode = "HOLD"
        optimization_reason = "Auto-fix recommended action is not clean pass"

    result = {
        "checked_at": utc_now(),
        "optimization_layer_status": layer_status,
        "next_step": next_step,
        "optimization_mode": optimization_mode,
        "optimization_reason": optimization_reason,
        "auto_fix_status": auto_fix_status,
        "recommended_action": recommended_action,
        "performance_status": performance_status,
        "price_optimizer_status": price_status,
        "title_optimizer_status": title_status,
        "latest_listing_id": latest_listing_id,
        "latest_sku": latest_sku,
        "selected_title": selected_title,
        "selected_price": selected_price,
        "selected_angle": selected_angle
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("OPTIMIZATION_STATUS_LAYER_V1:")
    print("optimization_layer_status:", result["optimization_layer_status"])
    print("next_step:", result["next_step"])
    print("optimization_mode:", result["optimization_mode"])
    print("selected_title:", result["selected_title"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
