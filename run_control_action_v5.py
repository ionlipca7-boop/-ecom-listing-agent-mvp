import json
import subprocess
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
RESOLVED_AUDIT_PATH = EXPORTS_DIR / "registry_resolve_action_v1_audit.json"
RESULT_PATH = EXPORTS_DIR / "control_action_v5.json"
def load_resolved_actions():
    if not RESOLVED_AUDIT_PATH.exists():
        return None, "RESOLVED_AUDIT_NOT_FOUND"
    data = json.loads(RESOLVED_AUDIT_PATH.read_text(encoding="utf-8"))
    if data.get("status") != "OK":
        return None, data.get("status", "RESOLVED_AUDIT_NOT_OK")
    actions = data.get("resolved_actions", [])
    if not actions:
        return None, "NO_RESOLVED_ACTIONS"
    return actions, "OK"
def run_update_quantity(action_item):
    cmd = [sys.executable, "run_increase_live_quantity_v1.py"]
    completed = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
    return {
        "executor_script": "run_increase_live_quantity_v1.py",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr
    }
def main():
    resolved_actions, status = load_resolved_actions()
    if status != "OK":
        audit = {
            "status": status,
            "resolved_audit_path": str(RESOLVED_AUDIT_PATH),
            "results_count": 0,
            "results": []
        }
        RESULT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CONTROL_ACTION_V5_FAILED")
        print("reason =", status)
        print("result_file =", RESULT_PATH)
        return
    results = []
    overall_status = "OK"
    print("CONTROL_ACTION_V5")
    print("resolved_actions_count =", len(resolved_actions))
    for item in resolved_actions:
        action_name = str(item.get("action", "")).strip()
        item_status = str(item.get("status", "")).strip()
        result = {
            "action": action_name,
            "product_key": item.get("product_key"),
            "quantity": item.get("quantity"),
            "sku": item.get("sku"),
            "offerId": item.get("offerId"),
            "resolved_status": item_status
        }
        if item_status != "OK":
            result["execution_status"] = "SKIPPED_RESOLVE_NOT_OK"
            overall_status = "PARTIAL"
        elif action_name == "update_quantity":
            exec_result = run_update_quantity(item)
            result["execution_status"] = "OK" if exec_result["returncode"] == 0 else "EXECUTOR_FAILED"
            result["executor"] = exec_result
            if exec_result["returncode"] != 0:
                overall_status = "PARTIAL"
        else:
            result["execution_status"] = "UNSUPPORTED_ACTION"
            overall_status = "PARTIAL"
        results.append(result)
        print("---")
        print("action =", result["action"])
        print("product_key =", result.get("product_key"))
        print("quantity =", result.get("quantity"))
        print("sku =", result.get("sku"))
        print("offerId =", result.get("offerId"))
        print("resolved_status =", result.get("resolved_status"))
        print("execution_status =", result.get("execution_status"))
    audit = {
        "status": overall_status,
        "resolved_audit_path": str(RESOLVED_AUDIT_PATH),
        "results_count": len(results),
        "results": results
    }
    RESULT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("---")
    print("final_status =", overall_status)
    print("result_file =", RESULT_PATH)
if __name__ == "__main__":
    main()
