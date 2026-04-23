import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
ACTION_PATH = EXPORTS_DIR / "control_action_v4.json"
AUDIT_PATH = EXPORTS_DIR / "batch_actions_v1_audit.json"

def main():
    if not ACTION_PATH.exists():
        audit = {
            "status": "ACTION_FILE_NOT_FOUND",
            "action_path": str(ACTION_PATH),
            "actions_count": 0,
            "execution_status": "SKIPPED"
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("BATCH_ACTIONS_V1_FAILED")
        print("reason = ACTION_FILE_NOT_FOUND")
        print("audit_file =", AUDIT_PATH)
        return

    action_data = json.loads(ACTION_PATH.read_text(encoding="utf-8"))
    actions = action_data.get("actions", [])
    actions_count = len(actions)

    if actions_count == 0:
        audit = {
            "status": "SKIPPED_NO_ACTIONS",
            "action_path": str(ACTION_PATH),
            "actions_count": actions_count,
            "execution_status": "SKIPPED"
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("BATCH_ACTIONS_V1_SKIPPED")
        print("reason = NO_ACTIONS")
        print("audit_file =", AUDIT_PATH)
        return

    cmd = ["py", "run_control_action_v5.py"]
    result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
    execution_status = "OK" if result.returncode == 0 else "EXECUTOR_FAILED"

    audit = {
        "status": "OK" if result.returncode == 0 else "PARTIAL",
        "action_path": str(ACTION_PATH),
        "actions_count": actions_count,
        "execution_status": execution_status,
        "executor": {
            "command": cmd,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    }

    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print("BATCH_ACTIONS_V1_DONE")
    print("actions_count =", actions_count)
    print("execution_status =", execution_status)
    print("executor_returncode =", result.returncode)
    print("audit_file =", AUDIT_PATH)

if __name__ == "__main__":
    main()
