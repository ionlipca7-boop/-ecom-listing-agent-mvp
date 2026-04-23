import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
COMPARE_FILE = EXPORTS_DIR / "post_reupload_compare_v1.json"
HANDOFF_FILE = EXPORTS_DIR / "manual_fixed_reupload_handoff_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "fix_cycle_closure_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def main():
    compare_data = read_json(COMPARE_FILE)
    handoff_data = read_json(HANDOFF_FILE)
    compare_status = str(compare_data.get("compare_status", "")).strip()
    fix_successful = str(compare_data.get("fix_successful", "")).strip()
    next_step_in = str(compare_data.get("next_step", "")).strip()
    export_fields = handoff_data.get("export_fields", [])
    if compare_status == "FIX_CONFIRMED" and fix_successful == "YES" and next_step_in == "CLOSE_FIX_CYCLE_AS_SUCCESS":
        closure_status = "SUCCESS"
        closure_gate = "CLOSED_AS_SUCCESS"
        next_step = "READY_FOR_NEXT_LISTING_OR_NEW_CASE"
    elif fix_successful == "YES":
        closure_status = "PARTIAL_SUCCESS"
        closure_gate = "REVIEW"
        next_step = "REVIEW_CLOSURE_STATUS"
    else:
        closure_status = "NOT_CLOSED"
        closure_gate = "OPEN"
        next_step = "RETURN_TO_FIX_OR_COMPARE"
    output = {}
    output["closure_status"] = closure_status
    output["closure_gate"] = closure_gate
    output["next_step"] = next_step
    output["compare_status"] = compare_status
    output["fix_successful"] = fix_successful
    output["closed_fields"] = export_fields
    output["source_files"] = {}
    output["source_files"]["post_reupload_compare"] = str(COMPARE_FILE)
    output["source_files"]["manual_fixed_reupload_handoff"] = str(HANDOFF_FILE)
    write_json(OUTPUT_FILE, output)
    print("FIX_CYCLE_CLOSURE_V1:")
    print("closure_status:", closure_status)
    print("closure_gate:", closure_gate)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
