import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
POST_FIX_FILE = EXPORTS_DIR / "post_fix_validation_v2.json"
APPLIED_FILE = EXPORTS_DIR / "applied_fix_result_v1.json"
PLAN_FILE = EXPORTS_DIR / "fix_execution_plan_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "template_revalidation_v1.json"

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

def extract_applied_fields(data):
    fields = []
    source_fields = data.get("fields")
    if isinstance(source_fields, dict):
        for key in source_fields.keys():
            value = normalize_name(key)
            if value != "":
                fields.append(value)
    return unique_list(fields)

def extract_plan_fields(data):
    fields = []
    plans = data.get("plans")
    if isinstance(plans, list):
        for plan in plans:
            if isinstance(plan, dict):
                repair_actions = plan.get("repair_actions")
                if isinstance(repair_actions, list):
                    for action in repair_actions:
                        if isinstance(action, dict):
                            value = normalize_name(action.get("target_field"))
                            if value != "":
                                fields.append(value)
    return unique_list(fields)

def main():
    post_fix = read_json(POST_FIX_FILE)
    applied = read_json(APPLIED_FILE)
    plan = read_json(PLAN_FILE)
    post_fix_status = post_fix.get("post_fix_validation_status", "")
    changed_fields = []
    for item in post_fix.get("changed_fields", []):
        value = normalize_name(item)
        if value != "":
            changed_fields.append(value)
    changed_fields = unique_list(changed_fields)
    applied_fields = extract_applied_fields(applied)
    plan_fields = extract_plan_fields(plan)
    missing_from_changed = []
    for field in plan_fields:
        if field not in changed_fields:
            missing_from_changed.append(field)
    missing_from_changed = unique_list(missing_from_changed)
    missing_from_applied = []
    for field in plan_fields:
        if field not in applied_fields:
            missing_from_applied.append(field)
    missing_from_applied = unique_list(missing_from_applied)
    field_alignment_ok = "NO"
    if len(missing_from_changed) == 0 and len(missing_from_applied) == 0:
        field_alignment_ok = "YES"
    if post_fix_status == "READY_FOR_REVALIDATION" and field_alignment_ok == "YES":
        revalidation_status = "READY"
        revalidation_gate = "OPEN"
        next_step = "RUN_REEXPORT_FROM_FIXED_DATA"
    elif post_fix_status == "READY_FOR_REVALIDATION":
        revalidation_status = "PARTIAL"
        revalidation_gate = "REVIEW"
        next_step = "REVIEW_FIELD_ALIGNMENT"
    else:
        revalidation_status = "BLOCKED"
        revalidation_gate = "CLOSED"
        next_step = "RETURN_TO_POST_FIX_REVIEW"
    output = {}
    output["revalidation_status"] = revalidation_status
    output["revalidation_gate"] = revalidation_gate
    output["next_step"] = next_step
    output["post_fix_status"] = post_fix_status
    output["field_alignment_ok"] = field_alignment_ok
    output["changed_fields"] = changed_fields
    output["applied_fields"] = applied_fields
    output["plan_fields"] = plan_fields
    output["missing_from_changed_fields"] = missing_from_changed
    output["missing_from_applied_fields"] = missing_from_applied
    output["post_fix_issue_count"] = post_fix.get("issue_count", 0)
    output["post_fix_covered_issues_count"] = post_fix.get("covered_issues_count", 0)
    output["post_fix_uncovered_issues_count"] = post_fix.get("uncovered_issues_count", 0)
    output["source_files"] = {}
    output["source_files"]["post_fix_validation"] = str(POST_FIX_FILE)
    output["source_files"]["applied_fix_result"] = str(APPLIED_FILE)
    output["source_files"]["fix_execution_plan"] = str(PLAN_FILE)
    write_json(OUTPUT_FILE, output)
    print("TEMPLATE_REVALIDATION_V1:")
    print("revalidation_status:", revalidation_status)
    print("revalidation_gate:", revalidation_gate)
    print("field_alignment_ok:", field_alignment_ok)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
