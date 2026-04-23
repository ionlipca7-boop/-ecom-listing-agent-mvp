import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
PREP_FILE = EXPORTS_DIR / "fixed_reupload_prep_v1.json"
VALIDATION_FILE = EXPORTS_DIR / "template_validation_on_fixed_export_v1.json"
REEXPORT_FILE = EXPORTS_DIR / "reexport_from_fixed_data_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "fixed_reupload_ready_status_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def normalize_name(value):
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = text.replace("itemspecifics", "item_specifics")
    text = text.replace("startprice", "price")
    text = text.replace("start_price", "price")
    text = text.replace(" ", "_")
    return text

def unique_list(values):
    result = []
    seen = set()
    for value in values:
        key = str(value)
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result

def extract_fields(data, key_name):
    fields = []
    items = data.get(key_name, [])
    if isinstance(items, list):
        for item in items:
            value = normalize_name(item)
            if value != "":
                fields.append(value)
    return unique_list(fields)

def main():
    prep = read_json(PREP_FILE)
    validation = read_json(VALIDATION_FILE)
    reexport = read_json(REEXPORT_FILE)
    prep_status = prep.get("prep_status", "")
    prep_gate = prep.get("prep_gate", "")
    validation_status = validation.get("validation_status", "")
    validation_gate = validation.get("validation_gate", "")
    reexport_status = reexport.get("reexport_status", "")
    reexport_gate = reexport.get("reexport_gate", "")
    export_fields = extract_fields(prep, "export_fields")
    payload_keys = extract_fields(prep, "payload_keys")
    missing_fields = []
    for field in export_fields:
        if field not in payload_keys:
            missing_fields.append(field)
    missing_fields = unique_list(missing_fields)
    payload_complete = "NO"
    if len(export_fields) != 0 and len(missing_fields) == 0:
        payload_complete = "YES"
    if prep_status == "READY" and prep_gate == "OPEN" and validation_status == "READY" and validation_gate == "OPEN" and reexport_status == "READY" and reexport_gate == "OPEN" and payload_complete == "YES":
        ready_status = "READY"
        ready_gate = "OPEN"
        next_step = "MANUAL_FIXED_REUPLOAD_ALLOWED"
    elif prep_status == "READY" and prep_gate == "OPEN":
        ready_status = "PARTIAL"
        ready_gate = "REVIEW"
        next_step = "REVIEW_REUPLOAD_READINESS"
    else:
        ready_status = "BLOCKED"
        ready_gate = "CLOSED"
        next_step = "RETURN_TO_REUPLOAD_PREP"
    output = {}
    output["ready_status"] = ready_status
    output["ready_gate"] = ready_gate
    output["next_step"] = next_step
    output["prep_status"] = prep_status
    output["prep_gate"] = prep_gate
    output["validation_status"] = validation_status
    output["validation_gate"] = validation_gate
    output["reexport_status"] = reexport_status
    output["reexport_gate"] = reexport_gate
    output["payload_complete"] = payload_complete
    output["export_fields"] = export_fields
    output["payload_keys"] = payload_keys
    output["missing_fields"] = missing_fields
    output["source_files"] = {}
    output["source_files"]["fixed_reupload_prep"] = str(PREP_FILE)
    output["source_files"]["fixed_export_validation"] = str(VALIDATION_FILE)
    output["source_files"]["reexport_from_fixed_data"] = str(REEXPORT_FILE)
    write_json(OUTPUT_FILE, output)
    print("FIXED_REUPLOAD_READY_STATUS_V1:")
    print("ready_status:", ready_status)
    print("ready_gate:", ready_gate)
    print("payload_complete:", payload_complete)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
