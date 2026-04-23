import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
CLOSURE_FILE = EXPORTS_DIR / "fix_cycle_closure_v1.json"
COMPARE_FILE = EXPORTS_DIR / "post_reupload_compare_v1.json"
PARSER_FILE = EXPORTS_DIR / "next_cycle_upload_result_parsed_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "fix_cycle_master_status_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def main():
    closure = read_json(CLOSURE_FILE)
    compare_data = read_json(COMPARE_FILE)
    parser_data = read_json(PARSER_FILE)
    closure_status = str(closure.get("closure_status", "")).strip()
    closure_gate = str(closure.get("closure_gate", "")).strip()
    compare_status = str(compare_data.get("compare_status", "")).strip()
    fix_successful = str(compare_data.get("fix_successful", "")).strip()
    parser_status = str(parser_data.get("parser_status", "")).strip()
    result_code = str(parser_data.get("result_code", "")).strip()
    closed_fields = closure.get("closed_fields", [])
    if closure_status == "SUCCESS" and closure_gate == "CLOSED_AS_SUCCESS" and compare_status == "FIX_CONFIRMED" and fix_successful == "YES" and parser_status == "SUCCESS":
        master_status = "READY"
        system_state = "FIX_LOOP_PROVEN"
        next_step = "READY_FOR_NEXT_LISTING_OR_NEW_CASE"
    else:
        master_status = "REVIEW"
        system_state = "FIX_LOOP_NOT_FULLY_CONFIRMED"
        next_step = "REVIEW_FIX_CYCLE_CHAIN"
    output = {}
    output["master_status"] = master_status
    output["system_state"] = system_state
    output["next_step"] = next_step
    output["closure_status"] = closure_status
    output["closure_gate"] = closure_gate
    output["compare_status"] = compare_status
    output["fix_successful"] = fix_successful
    output["parser_status"] = parser_status
    output["result_code"] = result_code
    output["closed_fields"] = closed_fields
    output["source_files"] = {}
    output["source_files"]["fix_cycle_closure"] = str(CLOSURE_FILE)
    output["source_files"]["post_reupload_compare"] = str(COMPARE_FILE)
    output["source_files"]["next_cycle_upload_result_parsed"] = str(PARSER_FILE)
    write_json(OUTPUT_FILE, output)
    print("FIX_CYCLE_MASTER_STATUS_V1:")
    print("master_status:", master_status)
    print("system_state:", system_state)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
