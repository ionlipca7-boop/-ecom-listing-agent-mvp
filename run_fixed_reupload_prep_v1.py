import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
VALIDATION_FILE = EXPORTS_DIR / "template_validation_on_fixed_export_v1.json"
REEXPORT_FILE = EXPORTS_DIR / "reexport_from_fixed_data_v1.json"
APPLIED_FILE = EXPORTS_DIR / "applied_fix_result_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "fixed_reupload_prep_v1.json"

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

def extract_payload(data):
    payload = {}
    fields = data.get("fields")
    if isinstance(fields, dict):
        for key, value in fields.items():
            normalized = normalize_name(key)
            if normalized != "":
                payload[normalized] = value
    return payload

def main():
    validation = read_json(VALIDATION_FILE)
    reexport = read_json(REEXPORT_FILE)
    applied = read_json(APPLIED_FILE)
    validation_status = validation.get("validation_status", "")
    validation_gate = validation.get("validation_gate", "")
    export_fields = extract_fields(reexport, "export_fields")
    payload_keys = extract_fields(validation, "payload_keys")
    applied_payload = extract_payload(applied)
    reupload_payload = {}
    for field in export_fields:
        if field in applied_payload:
            reupload_payload[field] = applied_payload[field]
    missing_payload_fields = []
    for field in export_fields:
        if field not in reupload_payload:
            missing_payload_fields.append(field)
    missing_payload_fields = unique_list(missing_payload_fields)
    payload_complete = "NO"
    if len(export_fields) != 0 and len(missing_payload_fields) == 0:
        payload_complete = "YES"
    if validation_status == "READY" and validation_gate == "OPEN" and payload_complete == "YES":
        prep_status = "READY"
        prep_gate = "OPEN"
        next_step = "READY_FOR_FIXED_REUPLOAD"
    elif validation_status == "READY" and validation_gate == "OPEN":
        prep_status = "PARTIAL"
        prep_gate = "REVIEW"
        next_step = "REVIEW_REUPLOAD_PAYLOAD"
    else:
        prep_status = "BLOCKED"
        prep_gate = "CLOSED"
        next_step = "RETURN_TO_FIXED_EXPORT_VALIDATION"
    output = {}
    output["prep_status"] = prep_status
    output["prep_gate"] = prep_gate
    output["next_step"] = next_step
    output["validation_status"] = validation_status
    output["validation_gate"] = validation_gate
    output["payload_complete"] = payload_complete
    output["export_fields"] = export_fields
    output["payload_keys"] = payload_keys
    output["missing_payload_fields"] = missing_payload_fields
    output["reupload_payload"] = reupload_payload
    output["source_files"] = {}
    output["source_files"]["fixed_export_validation"] = str(VALIDATION_FILE)
    output["source_files"]["reexport_from_fixed_data"] = str(REEXPORT_FILE)
    output["source_files"]["applied_fix_result"] = str(APPLIED_FILE)
    write_json(OUTPUT_FILE, output)
    print("FIXED_REUPLOAD_PREP_V1:")
    print("prep_status:", prep_status)
    print("prep_gate:", prep_gate)
    print("payload_complete:", payload_complete)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
