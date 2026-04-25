import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
APPLIED_FILE = EXPORTS_DIR / "applied_fix_result_v1.json"
ERROR_MAP_FILE = EXPORTS_DIR / "auto_fix_error_map_v2.json"
PLAN_FILE = EXPORTS_DIR / "fix_execution_plan_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "post_fix_validation_v2.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def to_list(value):
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]

def normalize_name(value):
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = text.replace("itemspecifics", "item_specifics")
    text = text.replace("startprice", "price")
    text = text.replace("start_price", "price")
    text = text.replace("brand", "brand")
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
    direct = data.get("fields")
    if isinstance(direct, dict):
        for key in direct.keys():
            value = normalize_name(key)
            if value != "":
                fields.append(value)
    extra_keys = ["applied_fields", "changed_fields", "fixed_fields"]
    for key in extra_keys:
        items = data.get(key)
        for item in to_list(items):
            value = normalize_name(item)
            if value != "":
                fields.append(value)
    return unique_list(fields)

def extract_plan_fields(plan_data):
    fields = []
    plans = plan_data.get("plans")
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

def extract_issue_records(error_map_data):
    issue_records = []
    items = error_map_data.get("issues")
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict):
                issue_records.append(item)
    return issue_records

def main():
    applied_data = read_json(APPLIED_FILE)
    error_map_data = read_json(ERROR_MAP_FILE)
    plan_data = read_json(PLAN_FILE)
    applied_fields = extract_applied_fields(applied_data)
    plan_fields = extract_plan_fields(plan_data)
    issue_records = extract_issue_records(error_map_data)
    covered_issue_details = []
    uncovered_issues = []
    for issue in issue_records:
        probable_fields = []
        raw_probable = issue.get("probable_fields")
        for item in to_list(raw_probable):
            value = normalize_name(item)
            if value != "":
                probable_fields.append(value)
        probable_fields = unique_list(probable_fields)
        matched_fields = []
        for field in probable_fields:
            if field in applied_fields:
                matched_fields.append(field)
        matched_fields = unique_list(matched_fields)
        detail = {}
        detail["issue_id"] = issue.get("issue_id", "")
        detail["issue_type"] = issue.get("issue_type", "unknown_issue")
        detail["probable_fields"] = probable_fields
        detail["matched_fields"] = matched_fields
        if len(matched_fields) != 0:
            detail["coverage_status"] = "COVERED"
            covered_issue_details.append(detail)
        else:
            detail["coverage_status"] = "UNCOVERED"
            uncovered_issues.append(detail)
    issue_count = len(issue_records)
    covered_count = len(covered_issue_details)
    uncovered_count = len(uncovered_issues)
    applied_count = len(applied_fields)
    if applied_count == 0:
        status = "NO_FIX_APPLIED"
        next_step = "REBUILD_FIX_PLAN"
    elif issue_count == 0:
        status = "READY_FOR_REVALIDATION"
        next_step = "RUN_TEMPLATE_REVALIDATION"
    elif covered_count == issue_count:
        status = "READY_FOR_REVALIDATION"
        next_step = "RUN_TEMPLATE_REVALIDATION"
    elif covered_count != 0:
        status = "PARTIAL_FIX"
        next_step = "REVIEW_UNCOVERED_ISSUES"
    else:
        status = "NO_FIX_APPLIED"
        next_step = "REBUILD_FIX_PLAN"
    output = {}
    output["validation_status"] = status
    output["post_fix_validation_status"] = status
    output["next_step"] = next_step
    output["issue_count"] = issue_count
    output["covered_issues_count"] = covered_count
    output["uncovered_issues_count"] = uncovered_count
    output["applied_patch_count"] = applied_count
    output["changed_fields"] = applied_fields
    output["plan_fields"] = plan_fields
    output["covered_issue_details"] = covered_issue_details
    output["uncovered_issues"] = uncovered_issues
    output["source_files"] = {}
    output["source_files"]["applied_fix_result"] = str(APPLIED_FILE)
    output["source_files"]["auto_fix_error_map"] = str(ERROR_MAP_FILE)
    output["source_files"]["fix_execution_plan"] = str(PLAN_FILE)
    write_json(OUTPUT_FILE, output)
    print("POST_FIX_VALIDATION_V2:")
    print("post_fix_validation_status:", status)
    print("issue_count:", issue_count)
    print("covered_issues_count:", covered_count)
    print("uncovered_issues_count:", uncovered_count)
    print("applied_patch_count:", applied_count)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
