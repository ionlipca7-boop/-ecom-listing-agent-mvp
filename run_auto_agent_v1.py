import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
STATUS_PATH = EXPORTS_DIR / "control_room_status_v1.json"
AUDIT_PATH = EXPORTS_DIR / "auto_agent_v1_audit.json"

def main():
    if not STATUS_PATH.exists():
        audit = {
            "status": "STATUS_FILE_NOT_FOUND",
            "status_path": str(STATUS_PATH),
            "execution_status": "SKIPPED"
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("AUTO_AGENT_V1_FAILED")
        print("reason = STATUS_FILE_NOT_FOUND")
        print("audit_file =", AUDIT_PATH)
        return

    status_data = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    system_status = str(status_data.get("system_status", "")).strip()

    if system_status != "OK":
        audit = {
            "status": "SKIPPED",
            "status_path": str(STATUS_PATH),
            "system_status": system_status,
            "execution_status": "SKIPPED"
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("AUTO_AGENT_V1_SKIPPED")
        print("system_status =", system_status)
        print("audit_file =", AUDIT_PATH)
        return

    cmd = ["py", "run_control_action_v5.py"]
    result = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)

    execution_status = "OK" if result.returncode == 0 else "EXECUTOR_FAILED"

    audit = {
        "status": "OK" if result.returncode == 0 else "PARTIAL",
        "status_path": str(STATUS_PATH),
        "system_status": system_status,
        "execution_status": execution_status,
        "executor": {
            "command": cmd,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    }

    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print("AUTO_AGENT_V1_DONE")
    print("system_status =", system_status)
    print("execution_status =", execution_status)
    print("executor_returncode =", result.returncode)
    print("audit_file =", AUDIT_PATH)

if __name__ == "__main__":
    main()
