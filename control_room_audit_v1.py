import json
from pathlib import Path

REQUIRED_FILES = [
    "run_control_room_v1.py",
    "create_real_publish_request_v1.py",
    "final_publish_manifest_v1.py",
    "approve_real_publish_v1.py",
    "run_full_publish_flow_v1.py",
    "control_room_report_v1.py",
    "prepare_real_ebay_upload_action_v1.py",
    "execute_real_ebay_upload_v1.py",
    "real_upload_handoff_report_v1.py",
    "run_control_room_dashboard_v1.py",
    "archive_control_room_run_v1.py",
    "history_index_v1.py",
    "history_inspector_v1.py",
    "decision_memory_v1.py",
    "upload_executor_v2.py"
]

REQUIRED_OUTPUTS = [
    "control_room_dashboard_v1.json",
    "control_room_history_index.json",
    "decision_memory_v1.json",
    "upload_execution_v2.json"
]


def check_files():
    missing = []
    for f in REQUIRED_FILES:
        if not Path(f).exists():
            missing.append(f)
    return missing


def check_outputs():
    missing = []
    for f in REQUIRED_OUTPUTS:
        if not Path(f).exists():
            missing.append(f)
    return missing


def main():
    missing_files = check_files()
    missing_outputs = check_outputs()

    system_ok = not missing_files and not missing_outputs

    result = {
        "system_ok": system_ok,
        "missing_files": missing_files,
        "missing_outputs": missing_outputs
    }

    with open("control_room_audit_v1.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("CONTROL ROOM AUDIT:")
    print(f"system_ok: {system_ok}")

    if missing_files:
        print("\nMISSING FILES:")
        for f in missing_files:
            print(f"- {f}")

    if missing_outputs:
        print("\nMISSING OUTPUTS:")
        for f in missing_outputs:
            print(f"- {f}")


if __name__ == "__main__":
    main()