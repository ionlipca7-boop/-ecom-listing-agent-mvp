import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "feedback_status_layer_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    parsed_data = read_json(EXPORTS_DIR / "ebay_upload_result_parsed_v1.json")
    feedback_data = read_json(EXPORTS_DIR / "control_room_upload_feedback_v1.json")
    router_data = read_json(EXPORTS_DIR / "ebay_upload_result_router_v1.json")
    inbox_data = read_json(EXPORTS_DIR / "prepare_upload_result_inbox_v1.json")

    parsed_summary = parsed_data.get("summary", {})
    router_summary = router_data.get("summary", {})

    parser_status = parsed_data.get("parser_status", "")
    feedback_status = feedback_data.get("upload_feedback_status", "")
    route_status = router_data.get("route_status", "")
    route_target = router_data.get("route_target", "")
    inbox_status = inbox_data.get("inbox_status", "")

    success_count = parsed_summary.get("success_count", 0)
    warning_count = parsed_summary.get("warning_count", 0)
    error_count = parsed_summary.get("error_count", 0)
    unknown_count = parsed_summary.get("unknown_count", 0)

    is_ready = parser_status == "SUCCESS" and feedback_status == "SUCCESS" and route_status == "CONFIRMED" and inbox_status == "READY"

    result = {
        "checked_at": utc_now(),
        "feedback_layer_status": "READY" if is_ready else "BLOCKED",
        "next_step": "BUILD_AUTO_FIX_LAYER" if is_ready else "FIX_FEEDBACK_INPUTS",
        "parser_status": parser_status,
        "feedback_status": feedback_status,
        "route_status": route_status,
        "route_target": route_target,
        "master_status": router_summary.get("master_status", ""),
        "latest_file": parsed_data.get("latest_file", ""),
        "success_count": success_count,
        "warning_count": warning_count,
        "error_count": error_count,
        "unknown_count": unknown_count,
        "inbox_status": inbox_status
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("FEEDBACK_STATUS_LAYER_V1:")
    print("feedback_layer_status:", result["feedback_layer_status"])
    print("next_step:", result["next_step"])
    print("parser_status:", result["parser_status"])
    print("feedback_status:", result["feedback_status"])
    print("route_status:", result["route_status"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
