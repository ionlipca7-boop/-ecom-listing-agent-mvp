import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REVALIDATION_FILE = EXPORTS_DIR / "template_revalidation_v1.json"
APPLIED_FILE = EXPORTS_DIR / "applied_fix_result_v1.json"
POST_FIX_FILE = EXPORTS_DIR / "post_fix_validation_v2.json"
OUTPUT_FILE = EXPORTS_DIR / "reexport_from_fixed_data_v1.json"

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

def extract_changed_fields(revalidation_data):
    fields = []
    items = revalidation_data.get("changed_fields", [])
    if isinstance(items, list):
        for item in items:
            value = normalize_name(item)
            if value != "":
                fields.append(value)
    return unique_list(fields)

def extract_fixed_payload(applied_data):
    payload = {}
    fields = applied_data.get("fields")
    if isinstance(fields, dict):
        for key, value in fields.items():
            normalized = normalize_name(key)
            if normalized != "":
                payload[normalized] = value
    return payload

def main():
    revalidation = read_json(REVALIDATION_FILE)
    applied = read_json(APPLIED_FILE)
    post_fix = read_json(POST_FIX_FILE)
    revalidation_status = revalidation.get("revalidation_status", "")
    revalidation_gate = revalidation.get("revalidation_gate", "")
    changed_fields = extract_changed_fields(revalidation)
    fixed_payload = extract_fixed_payload(applied)
    export_fields = []
    export_payload = {}
    for field in changed_fields:
        if field in fixed_payload:
            export_fields.append(field)
            export_payload[field] = fixed_payload[field]
    export_fields = unique_list(export_fields)
    export_count = len(export_fields)
    if revalidation_status == "READY" and revalidation_gate == "OPEN" and export_count != 0:
        reexport_status = "READY"
        reexport_gate = "OPEN"
        next_step = "RUN_TEMPLATE_VALIDATION_ON_FIXED_EXPORT"
    elif revalidation_status == "READY" and revalidation_gate == "OPEN":
        reexport_status = "PARTIAL"
        reexport_gate = "REVIEW"
        next_step = "REVIEW_FIXED_PAYLOAD"
    else:
        reexport_status = "BLOCKED"
        reexport_gate = "CLOSED"
        next_step = "RETURN_TO_REVALIDATION_GATE"
    output = {}
    output["reexport_status"] = reexport_status
    output["reexport_gate"] = reexport_gate
    output["next_step"] = next_step
    output["revalidation_status"] = revalidation_status
    output["revalidation_gate"] = revalidation_gate
    output["post_fix_status"] = post_fix.get("post_fix_validation_status", "")
    output["export_fields_count"] = export_count
    output["export_fields"] = export_fields
    output["fixed_payload"] = export_payload
    output["source_files"] = {}
    output["source_files"]["template_revalidation"] = str(REVALIDATION_FILE)
    output["source_files"]["applied_fix_result"] = str(APPLIED_FILE)
    output["source_files"]["post_fix_validation"] = str(POST_FIX_FILE)
    write_json(OUTPUT_FILE, output)
    print("REEXPORT_FROM_FIXED_DATA_V1:")
    print("reexport_status:", reexport_status)
    print("reexport_gate:", reexport_gate)
    print("export_fields_count:", export_count)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
