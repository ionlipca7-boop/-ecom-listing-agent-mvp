import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
APPLIED_FILE = EXPORTS_DIR / "applied_fix_result_v1.json"
ERROR_MAP_FILE = EXPORTS_DIR / "auto_fix_error_map_v2.json"
PLAN_FILE = EXPORTS_DIR / "fix_execution_plan_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "post_fix_validation_v1.json"

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
    patch_keys = ["applied_patches", "applied_actions", "patches", "actions", "queue_items"]
    for key in patch_keys:
        items = data.get(key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    candidates = []
                    candidates.extend(to_list(item.get("field")))
                    candidates.extend(to_list(item.get("target_field")))
                    candidates.extend(to_list(item.get("mapped_field")))
                    candidates.extend(to_list(item.get("patch_type")))
                    candidates.extend(to_list(item.get("action_type")))
                    candidates.extend(to_list(item.get("name")))
                    for candidate in candidates:
                        value = normalize_name(candidate)
                        if value != "":
                            fields.append(value)
    direct_keys = ["applied_fields", "changed_fields", "fixed_fields"]
    for key in direct_keys:
        items = data.get(key)
        for item in to_list(items):
            value = normalize_name(item)
            if value != "":
                fields.append(value)
    return unique_list(fields)

def extract_issue_records(error_map_data):
    issue_records = []
    keys = ["issues", "mapped_issues", "error_map", "records"]
    for key in keys:
        items = error_map_data.get(key)
        if isinstance(items, list):
            if len(items) != 0:
                for item in items:
                    if isinstance(item, dict):
                        issue_records.append(item)
                if len(issue_records) != 0:
                    return issue_records
    probable = error_map_data.get("probable_fields")
    if isinstance(probable, list):
        if len(probable) != 0:
            fallback = {}
            fallback["issue"] = error_map_data.get("error_message", "unknown_issue")
            fallback["probable_fields"] = probable
            issue_records.append(fallback)
    return issue_records

def extract_plan_fields(plan_data):
    fields = []
    keys = ["actions", "repair_actions", "planned_actions"]
    for key in keys:
        items = plan_data.get(key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    candidates = []
                    candidates.extend(to_list(item.get("field")))
                    candidates.extend(to_list(item.get("target_field")))
                    candidates.extend(to_list(item.get("repair_target")))
                    candidates.extend(to_list(item.get("action_type")))
                    candidates.extend(to_list(item.get("name")))
                    for candidate in candidates:
                        value = normalize_name(candidate)
                        if value != "":
                            fields.append(value)
    return unique_list(fields)

def main():
    applied_data = read_json(APPLIED_FILE)
    error_map_data = read_json(ERROR_MAP_FILE)
    plan_data = read_json(PLAN_FILE)
    applied_fields = extract_applied_fields(applied_data)
    plan_fields = extract_plan_fields(plan_data)
    issue_records = extract_issue_records(error_map_data)
    issue_count = len(issue_records)
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
        issue_name = issue.get("issue", issue.get("error_message", "unknown_issue"))
        detail = {}
        detail["issue"] = issue_name
        detail["probable_fields"] = probable_fields
        detail["matched_fields"] = matched_fields
        if len(matched_fields) != 0:
            detail["coverage_status"] = "COVERED"
            covered_issue_details.append(detail)
        else:
            detail["coverage_status"] = "UNCOVERED"
            uncovered_issues.append(detail)
    applied_count = len(applied_fields)
    covered_count = len(covered_issue_details)
    uncovered_count = len(uncovered_issues)
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
    print("POST_FIX_VALIDATION_V1:")
    print("post_fix_validation_status:", status)
    print("issue_count:", issue_count)
    print("covered_issues_count:", covered_count)
    print("uncovered_issues_count:", uncovered_count)
    print("applied_patch_count:", applied_count)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
