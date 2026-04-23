import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
UPLOAD_RESULTS_DIR = BASE_DIR / "storage" / "upload_results"
TRIGGER_FILE = EXPORTS_DIR / "next_cycle_parser_trigger_v1.json"
INPUT_FILE = UPLOAD_RESULTS_DIR / "ebay_result_after_fixed_reupload_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "next_cycle_upload_result_parsed_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()

def main():
    trigger = read_json(TRIGGER_FILE)
    raw = read_json(INPUT_FILE)
    trigger_status = trigger.get("trigger_status", "")
    trigger_gate = trigger.get("trigger_gate", "")
    trigger_next_step = trigger.get("next_step", "")
    result_status = normalize_text(raw.get("result_status")).upper()
    result_code = normalize_text(raw.get("result_code")).upper()
    message = normalize_text(raw.get("message"))
    sku = normalize_text(raw.get("sku"))
    parser_status = "UNKNOWN"
    status_bucket = "UNKNOWN"
    if result_status == "SUCCESS":
        parser_status = "SUCCESS"
        status_bucket = "SUCCESS"
    elif result_status == "ERROR":
        parser_status = "HAS_ERRORS"
        status_bucket = "ERROR"
    elif result_status == "WARNING":
        parser_status = "HAS_WARNINGS"
        status_bucket = "WARNING"
    ready_for_compare = "NO"
    if trigger_status == "READY" and trigger_gate == "OPEN" and trigger_next_step == "RUN_UPLOAD_RESULT_PARSER_ON_NEW_FILE":
        ready_for_compare = "YES"
    if parser_status == "SUCCESS" and ready_for_compare == "YES":
        next_step = "RUN_POST_REUPLOAD_COMPARE"
    elif parser_status == "HAS_ERRORS" and ready_for_compare == "YES":
        next_step = "RUN_SECOND_FIX_CYCLE_OR_COMPARE"
    else:
        next_step = "REVIEW_NEXT_CYCLE_RESULT"
    output = {}
    output["parser_status"] = parser_status
    output["status_bucket"] = status_bucket
    output["next_step"] = next_step
    output["ready_for_compare"] = ready_for_compare
    output["result_status"] = result_status
    output["result_code"] = result_code
    output["message"] = message
    output["sku"] = sku
    output["source_files"] = {}
    output["source_files"]["trigger_file"] = str(TRIGGER_FILE)
    output["source_files"]["input_file"] = str(INPUT_FILE)
    write_json(OUTPUT_FILE, output)
    print("NEXT_CYCLE_UPLOAD_RESULT_PARSER_V1:")
    print("parser_status:", parser_status)
    print("status_bucket:", status_bucket)
    print("ready_for_compare:", ready_for_compare)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
