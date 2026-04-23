import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SOURCE_JSON = EXPORTS_DIR / "ebay_upload_result_parsed_v1.json"
OUTPUT_JSON = EXPORTS_DIR / "control_room_upload_feedback_v1.json"

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def main():
    data = load_json(SOURCE_JSON)
    parser_status = data.get("parser_status", "NO_INPUT")
    summary = data.get("summary", {})

    if parser_status == "NO_INPUT":
        upload_feedback_status = "WAITING_RESULT"
        next_step = "PLACE_EBAY_RESULT_FILE_IN_UPLOAD_RESULTS" 
    elif summary.get("error_count", 0) > 0:
        upload_feedback_status = "HAS_ERRORS"
        next_step = "REVIEW_EBAY_UPLOAD_ERRORS" 
    elif summary.get("warning_count", 0) > 0:
        upload_feedback_status = "HAS_WARNINGS"
        next_step = "REVIEW_EBAY_UPLOAD_WARNINGS" 
    elif summary.get("success_count", 0) > 0:
        upload_feedback_status = "SUCCESS"
        next_step = "UPLOAD_CONFIRMED" 
    else:
        upload_feedback_status = "UNKNOWN"
        next_step = "CHECK_UPLOAD_RESULT_FILE" 

    output = {
        "upload_feedback_status": upload_feedback_status,
        "parser_status": parser_status,
        "latest_file": data.get("latest_file", ""),
        "success_count": summary.get("success_count", 0),
        "warning_count": summary.get("warning_count", 0),
        "error_count": summary.get("error_count", 0),
        "unknown_count": summary.get("unknown_count", 0),
        "next_step": next_step,
    }

    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("CONTROL_ROOM_UPLOAD_FEEDBACK_V1:")
    print(f"upload_feedback_status: {upload_feedback_status}")
    print(f"parser_status: {parser_status}")
    print(f"success_count: {summary.get('success_count', 0)}")
    print(f"warning_count: {summary.get('warning_count', 0)}")
    print(f"error_count: {summary.get('error_count', 0)}")
    print(f"next_step: {next_step}")
    print(f"output_json: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
