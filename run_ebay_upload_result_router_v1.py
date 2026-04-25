import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
FEEDBACK_FILE = EXPORTS_DIR / "control_room_upload_feedback_v1.json"
MASTER_FILE = EXPORTS_DIR / "control_room_master_status_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "ebay_upload_result_router_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    feedback = read_json(FEEDBACK_FILE)
    master = read_json(MASTER_FILE)

    feedback_status = "MISSING"
    parser_status = "MISSING"
    master_status = "MISSING"

    if feedback:
        feedback_status = feedback.get("upload_feedback_status", "MISSING")
        parser_status = feedback.get("parser_status", "MISSING")
        success_count = feedback.get("success_count", 0)
        warning_count = feedback.get("warning_count", 0)
        error_count = feedback.get("error_count", 0)

    if master:
        master_status = master.get("master_status", "MISSING")

    if feedback_status == "SUCCESS":
        route_status = "CONFIRMED"
        route_target = "POST_UPLOAD_CONFIRMED_FLOW"
        next_step = "READY_FOR_PERFORMANCE_LAYER"
    elif feedback_status == "WAITING_RESULT":
        route_status = "WAITING_RESULT"
        route_target = "UPLOAD_RESULT_INBOX"
        next_step = "PLACE_EBAY_RESULT_FILE_IN_UPLOAD_RESULTS"
    elif feedback_status == "WARNING":
        route_status = "REVIEW"
        route_target = "MANUAL_REVIEW_FLOW"
        next_step = "REVIEW_UPLOAD_WARNINGS"
    elif feedback_status == "HAS_WARNINGS":
        route_status = "REVIEW"
        route_target = "MANUAL_REVIEW_FLOW"
        next_step = "REVIEW_UPLOAD_WARNINGS"
    elif feedback_status == "ERROR":
        route_status = "FIX_REQUIRED"
        route_target = "AUTO_FIX_OR_MANUAL_FIX_FLOW"
        next_step = "RUN_AUTO_FIX_OR_MANUAL_REPAIR"
    elif feedback_status == "HAS_ERRORS":
        route_status = "FIX_REQUIRED"
        route_target = "AUTO_FIX_OR_MANUAL_FIX_FLOW"
        next_step = "RUN_AUTO_FIX_OR_MANUAL_REPAIR"
    else:
        route_status = "UNKNOWN"
        route_target = "CHECK_FEEDBACK_LAYER"
        next_step = "CHECK_UPLOAD_FEEDBACK_LAYER"

    output = {
        "route_status": route_status,
        "route_target": route_target,
        "next_step": next_step,
        "summary": {
            "master_status": master_status,
            "feedback_status": feedback_status,
            "parser_status": parser_status,
            "success_count": success_count,
            "warning_count": warning_count,
            "error_count": error_count
        },
        "inputs": {
            "feedback_file": str(FEEDBACK_FILE),
            "master_file": str(MASTER_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("EBAY_UPLOAD_RESULT_ROUTER_V1:")
    print("route_status:", output["route_status"])
    print("route_target:", output["route_target"])
    print("master_status:", output["summary"]["master_status"])
    print("feedback_status:", output["summary"]["feedback_status"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
