import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REEXPORT_FILE = EXPORTS_DIR / "reexport_from_fixed_data_v1.json"
REVALIDATION_FILE = EXPORTS_DIR / "template_revalidation_v1.json"
POST_FIX_FILE = EXPORTS_DIR / "post_fix_validation_v2.json"
OUTPUT_FILE = EXPORTS_DIR / "template_validation_on_fixed_export_v1.json"

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

def main():
    reexport = read_json(REEXPORT_FILE)
    revalidation = read_json(REVALIDATION_FILE)
    post_fix = read_json(POST_FIX_FILE)
    reexport_status = reexport.get("reexport_status", "")
    reexport_gate = reexport.get("reexport_gate", "")
    revalidation_status = revalidation.get("revalidation_status", "")
    field_alignment_ok = revalidation.get("field_alignment_ok", "NO")
    export_fields = []
    items = reexport.get("export_fields", [])
    if isinstance(items, list):
        for item in items:
            value = normalize_name(item)
            if value != "":
                export_fields.append(value)
    export_fields = unique_list(export_fields)
    fixed_payload = reexport.get("fixed_payload", {})
    payload_keys = []
    if isinstance(fixed_payload, dict):
        for key in fixed_payload.keys():
            value = normalize_name(key)
            if value != "":
                payload_keys.append(value)
    payload_keys = unique_list(payload_keys)
    missing_in_payload = []
    for field in export_fields:
        if field not in payload_keys:
            missing_in_payload.append(field)
    missing_in_payload = unique_list(missing_in_payload)
    payload_complete = "NO"
    if len(export_fields) != 0 and len(missing_in_payload) == 0:
        payload_complete = "YES"
    if reexport_status == "READY" and reexport_gate == "OPEN" and revalidation_status == "READY" and field_alignment_ok == "YES" and payload_complete == "YES":
        validation_status = "READY"
        validation_gate = "OPEN"
        next_step = "RUN_FIXED_REUPLOAD_PREP"
    elif reexport_status == "READY" and reexport_gate == "OPEN":
        validation_status = "PARTIAL"
        validation_gate = "REVIEW"
        next_step = "REVIEW_FIXED_EXPORT_PAYLOAD"
    else:
        validation_status = "BLOCKED"
        validation_gate = "CLOSED"
        next_step = "RETURN_TO_REEXPORT_GATE"
    output = {}
    output["validation_status"] = validation_status
    output["validation_gate"] = validation_gate
    output["next_step"] = next_step
    output["reexport_status"] = reexport_status
    output["reexport_gate"] = reexport_gate
    output["revalidation_status"] = revalidation_status
    output["field_alignment_ok"] = field_alignment_ok
    output["payload_complete"] = payload_complete
    output["export_fields"] = export_fields
    output["payload_keys"] = payload_keys
    output["missing_in_payload"] = missing_in_payload
    output["post_fix_status"] = post_fix.get("post_fix_validation_status", "")
    output["source_files"] = {}
    output["source_files"]["reexport"] = str(REEXPORT_FILE)
    output["source_files"]["revalidation"] = str(REVALIDATION_FILE)
    output["source_files"]["post_fix_validation"] = str(POST_FIX_FILE)
    write_json(OUTPUT_FILE, output)
    print("TEMPLATE_VALIDATION_ON_FIXED_EXPORT_V1:")
    print("validation_status:", validation_status)
    print("validation_gate:", validation_gate)
    print("payload_complete:", payload_complete)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
