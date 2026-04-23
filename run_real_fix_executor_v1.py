import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "fix_execution_plan_v1.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "real_fix_executor_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def safe_read_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return True, data, None
    except FileNotFoundError:
        return False, None, "input file not found: " + str(path)
    except json.JSONDecodeError as exc:
        return False, None, "invalid json: " + str(exc)
    except Exception as exc:
        return False, None, "unexpected read error: " + str(exc)

def target_file_for_action(repair_action):
    mapping = {}
    mapping["fill_required_aspect"] = "ebay_upload_ready_v2.csv_or_template_mapper"
    mapping["repair_item_specifics"] = "run_ebay_template_mapper_v2.py"
    mapping["normalize_price"] = "run_price_optimizer_v1.py"
    mapping["rebuild_title"] = "run_ai_title_optimizer_v1.py"
    mapping["rebuild_description"] = "run_storage_to_listing_v1.py"
    mapping["repair_images"] = "run_photo_manifest_v1.py"
    mapping["repair_shipping"] = "run_ebay_template_mapper_v2.py"
    mapping["repair_payment_policy"] = "business_policy_layer"
    mapping["repair_return_policy"] = "business_policy_layer"
    mapping["repair_business_policy"] = "business_policy_layer"
    mapping["manual_review"] = "operator_review"
    return mapping.get(repair_action, "unknown_target")

def main():
    ok, data, error = safe_read_json(INPUT_FILE)
    result = {}
    zero = int("0")
    one = int("1")
    result["executed_at"] = utc_now()
    result["source_file"] = str(INPUT_FILE)
    result["output_file"] = str(OUTPUT_FILE)
    result["executor_status"] = "READY"
    result["execution_mode"] = "DRY_RUN_QUEUE"
    result["issues_count"] = zero
    result["action_count"] = zero
    result["queued_actions"] = zero
    result["manual_actions"] = zero
    result["queue"] = []
    result["next_step"] = "APPLY_FIXES_TO_LISTING_DATA"
    if not ok:
        result["executor_status"] = "ERROR"
        result["error"] = error
        result["next_step"] = "FIX_EXECUTION_PLAN_INPUT"
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REAL_FIX_EXECUTOR_V1:")
        print("executor_status:", result["executor_status"])
        print("error:", error)
        print("output_file:", OUTPUT_FILE.name)
        return
    plans = data.get("plans", [])
    result["issues_count"] = len(plans)
    queued_count = zero
    manual_count = zero
    action_count = zero
    for plan in plans:
        issue_id = plan.get("issue_id", "ISSUE")
        actions = plan.get("repair_actions", [])
        action_count = action_count + len(actions)
        for action in actions:
            queue_record = {}
            queue_record["issue_id"] = issue_id
            queue_record["step_id"] = action.get("step_id")
            queue_record["target_field"] = action.get("target_field")
            queue_record["repair_action"] = action.get("repair_action")
            queue_record["source_layer"] = action.get("source_layer")
            queue_record["instruction"] = action.get("instruction")
            queue_record["target_file"] = target_file_for_action(action.get("repair_action"))
            if action.get("automation_ready") == "YES":
                queue_record["execution_status"] = "QUEUED"
                queue_record["executor_decision"] = "AUTO_READY"
                queued_count = queued_count + one
            else:
                queue_record["execution_status"] = "MANUAL_REVIEW"
                queue_record["executor_decision"] = "REVIEW_REQUIRED"
                manual_count = manual_count + one
            result["queue"].append(queue_record)
    result["action_count"] = action_count
    result["queued_actions"] = queued_count
    result["manual_actions"] = manual_count
    if manual_count != zero:
        result["executor_status"] = "PARTIAL_READY"
        result["next_step"] = "RUN_AUTO_AND_REVIEW_MANUAL"
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REAL_FIX_EXECUTOR_V1:")
    print("executor_status:", result["executor_status"])
    print("issues_count:", result["issues_count"])
    print("action_count:", result["action_count"])
    print("queued_actions:", result["queued_actions"])
    print("manual_actions:", result["manual_actions"])
    print("next_step:", result["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
