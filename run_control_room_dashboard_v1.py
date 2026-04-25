import json
import subprocess
from datetime import datetime, UTC
from pathlib import Path

DASHBOARD_FILE = Path("control_room_dashboard_v1.json")
DECISION_FILE = Path("decision_memory_v1.json")


def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def load_decision():
    if not DECISION_FILE.exists():
        return {
            "system_state": "UNKNOWN",
            "decision": "NO_DECISION"
        }

    with open(DECISION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    decision_data = load_decision()

    dashboard = {
        "checked_at": utc_now(),
        "dashboard_status": "READY",
        "last_package": "package_20260414_070314",
        "next_step": "UPLOAD_TO_EBAY_MANUALLY_OR_CONNECT_REAL_API",
        "system_state": decision_data.get("system_state"),
        "decision": decision_data.get("decision"),
        "summary": {
            "report_status": "OK",
            "handoff_status": "READY_FOR_MANUAL_UPLOAD"
        }
    }

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)

    print("CONTROL_ROOM_DASHBOARD:")
    print(f"last_package: {dashboard['last_package']}")
    print(f"dashboard_status: {dashboard['dashboard_status']}")
    print(f"system_state: {dashboard['system_state']}")
    print(f"decision: {dashboard['decision']}")
    print(f"next_step: {dashboard['next_step']}")
    print(f"output_file: {DASHBOARD_FILE}")

    # --- AUTO ARCHIVE HOOK ---
    print("\nAUTO ARCHIVE HOOK:\n")

    subprocess.run("python archive_control_room_run_v1.py", shell=True)
    subprocess.run("python history_index_v1.py", shell=True)
    subprocess.run("python history_inspector_v1.py", shell=True)
    subprocess.run("python decision_memory_v1.py", shell=True)


if __name__ == "__main__":
    main()