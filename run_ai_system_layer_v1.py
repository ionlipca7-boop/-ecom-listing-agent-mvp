import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "ai_system_layer_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    optimization_data = read_json(EXPORTS_DIR / "optimization_status_layer_v1.json")
    portable_data = read_json(EXPORTS_DIR / "portable_publish_bundle_v1.json")
    one_click_data = read_json(EXPORTS_DIR / "one_click_package_ready_v1.json")
    feedback_data = read_json(EXPORTS_DIR / "feedback_status_layer_v1.json")

    optimization_status = optimization_data.get("optimization_layer_status", "")
    portable_status = portable_data.get("bundle_status", "")
    one_click_status = one_click_data.get("one_click_package_status", "")
    feedback_status = feedback_data.get("feedback_layer_status", "")

    system_status = "READY"
    next_step = "BUILD_LOCAL_APP_LAUNCHER" 
    system_mode = "AI_ORCHESTRATION_READY"
    system_reason = "Core pipeline, feedback and optimization are ready"

    if optimization_status != "READY":
        system_status = "BLOCKED"
        next_step = "FIX_OPTIMIZATION_LAYER"
        system_mode = "WAIT"
        system_reason = "Optimization layer is not ready"
    elif portable_status != "READY":
        system_status = "BLOCKED"
        next_step = "FIX_PORTABLE_BUNDLE"
        system_mode = "WAIT"
        system_reason = "Portable bundle is not ready"
    elif one_click_status != "READY":
        system_status = "BLOCKED"
        next_step = "FIX_ONE_CLICK_PACKAGE"
        system_mode = "WAIT"
        system_reason = "One-click package is not ready"
    elif feedback_status != "READY":
        system_status = "BLOCKED"
        next_step = "FIX_FEEDBACK_LAYER"
        system_mode = "WAIT"
        system_reason = "Feedback layer is not ready"

    result = {
        "checked_at": utc_now(),
        "ai_system_status": system_status,
        "next_step": next_step,
        "system_mode": system_mode,
        "system_reason": system_reason,
        "optimization_layer_status": optimization_status,
        "portable_bundle_status": portable_status,
        "one_click_package_status": one_click_status,
        "feedback_layer_status": feedback_status,
        "package_id": portable_data.get("package_id", ""),
        "bundle_dir": portable_data.get("bundle_dir", ""),
        "selected_title": optimization_data.get("selected_title", ""),
        "selected_price": optimization_data.get("selected_price", ""),
        "selected_angle": optimization_data.get("selected_angle", ""),
        "latest_listing_id": optimization_data.get("latest_listing_id", ""),
        "latest_sku": optimization_data.get("latest_sku", "")
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("AI_SYSTEM_LAYER_V1:")
    print("ai_system_status:", result["ai_system_status"])
    print("next_step:", result["next_step"])
    print("system_mode:", result["system_mode"])
    print("selected_title:", result["selected_title"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
