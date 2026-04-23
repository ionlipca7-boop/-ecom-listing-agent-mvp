import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
UPLOAD_RESULTS_DIR = BASE_DIR / "storage" / "upload_results"
OLD_FILE = UPLOAD_RESULTS_DIR / "ebay_result_sample_error_v1.json"
NEW_FILE = EXPORTS_DIR / "next_cycle_upload_result_parsed_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "post_reupload_compare_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def normalize_text(value):
    if value is None:
        return ""
    return str(value).strip().upper()

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def main():
    old_data = read_json(OLD_FILE)
    new_data = read_json(NEW_FILE)
    old_status = normalize_text(old_data.get("result_status"))
    old_code = normalize_text(old_data.get("result_code"))
    old_message = str(old_data.get("message", ""))
    new_parser_status = normalize_text(new_data.get("parser_status"))
    new_status_bucket = normalize_text(new_data.get("status_bucket"))
    new_code = normalize_text(new_data.get("result_code"))
    new_message = str(new_data.get("message", ""))
    status_changed = "NO"
    if old_status != new_status_bucket:
        status_changed = "YES"
    fix_successful = "NO"
    if old_status == "ERROR" and new_parser_status == "SUCCESS":
        fix_successful = "YES"
    if fix_successful == "YES":
        compare_status = "FIX_CONFIRMED"
        next_step = "CLOSE_FIX_CYCLE_AS_SUCCESS"
    elif status_changed == "YES":
        compare_status = "STATUS_CHANGED_REVIEW"
        next_step = "REVIEW_CHANGED_RESULT"
    else:
        compare_status = "NO_IMPROVEMENT"
        next_step = "RUN_SECOND_FIX_CYCLE"
    output = {}
    output["compare_status"] = compare_status
    output["next_step"] = next_step
    output["fix_successful"] = fix_successful
    output["status_changed"] = status_changed
    output["old_status"] = old_status
    output["old_code"] = old_code
    output["old_message"] = old_message
    output["new_parser_status"] = new_parser_status
    output["new_status_bucket"] = new_status_bucket
    output["new_code"] = new_code
    output["new_message"] = new_message
    output["source_files"] = {}
    output["source_files"]["old_file"] = str(OLD_FILE)
    output["source_files"]["new_file"] = str(NEW_FILE)
    write_json(OUTPUT_FILE, output)
    print("POST_REUPLOAD_COMPARE_V1:")
    print("compare_status:", compare_status)
    print("fix_successful:", fix_successful)
    print("status_changed:", status_changed)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
