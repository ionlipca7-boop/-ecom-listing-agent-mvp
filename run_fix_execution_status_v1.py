import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "fix_execution_plan_v1.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "fix_execution_status_v1.json"

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

def main():
    ok, data, error = safe_read_json(INPUT_FILE)
    result = {}
    zero = int("0")
    result["checked_at"] = utc_now()
    result["source_file"] = str(INPUT_FILE)
    result["output_file"] = str(OUTPUT_FILE)
    result["fix_execution_status"] = "READY"
    result["issues_count"] = zero
    result["action_count"] = zero
    result["automation_ready_actions"] = zero
    result["manual_review_actions"] = zero
    result["next_step"] = "BUILD_REAL_FIX_EXECUTOR"
    if not ok:
        result["fix_execution_status"] = "ERROR"
        result["error"] = error
        result["next_step"] = "FIX_INPUT_FILE"
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("FIX_EXECUTION_STATUS_V1:")
        print("fix_execution_status:", result["fix_execution_status"])
        print("error:", error)
        print("output_file:", OUTPUT_FILE.name)
        return
    plans = data.get("plans", [])
    result["issues_count"] = len(plans)
    total_actions = zero
    auto_actions = zero
    manual_actions = zero
    for plan in plans:
        actions = plan.get("repair_actions", [])
        total_actions = total_actions + len(actions)
        for action in actions:
            if action.get("automation_ready") == "YES":
                auto_actions = auto_actions + int("1")
            else:
                manual_actions = manual_actions + int("1")
    result["action_count"] = total_actions
    result["automation_ready_actions"] = auto_actions
    result["manual_review_actions"] = manual_actions
    if total_actions == zero:
        result["fix_execution_status"] = "NO_ACTIONS"
        result["next_step"] = "REVIEW_FIX_PLAN"
    elif manual_actions > zero:
        result["fix_execution_status"] = "PARTIAL_AUTOMATION"
        result["next_step"] = "RUN_AUTO_ACTIONS_AND_REVIEW_MANUAL"
    else:
        result["fix_execution_status"] = "READY"
        result["next_step"] = "BUILD_REAL_FIX_EXECUTOR"
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("FIX_EXECUTION_STATUS_V1:")
    print("fix_execution_status:", result["fix_execution_status"])
    print("issues_count:", result["issues_count"])
    print("action_count:", result["action_count"])
    print("automation_ready_actions:", result["automation_ready_actions"])
    print("manual_review_actions:", result["manual_review_actions"])
    print("next_step:", result["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
