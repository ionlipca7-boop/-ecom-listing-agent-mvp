import json
from datetime import datetime, UTC
from pathlib import Path

from history_inspector_v2 import inspect_history
from run_stability_guard_v1 import evaluate_stability

DASHBOARD_FILE = Path("control_room_dashboard_v2.json")


def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def main():
    inspector = inspect_history()
    stability = evaluate_stability()

    dashboard = {
        "checked_at": utc_now(),
        "dashboard_status": "READY",
        "system_state": stability.get("system_state", "UNKNOWN"),
        "valid_runs": inspector.get("valid_runs", 0),
        "invalid_runs": inspector.get("invalid_runs", 0),
        "last_valid_run": inspector.get("last_valid_run", {}),
        "next_step": "UPLOAD_TO_EBAY_MANUALLY_OR_CONNECT_REAL_API"
    }

    with open(DASHBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2, ensure_ascii=False)

    print("CONTROL_ROOM_DASHBOARD_V2:")
    print(f"dashboard_status: {dashboard['dashboard_status']}")
    print(f"system_state: {dashboard['system_state']}")
    print(f"valid_runs: {dashboard['valid_runs']}")
    print(f"invalid_runs: {dashboard['invalid_runs']}")
    print(f"next_step: {dashboard['next_step']}")
    print(f"output_file: {DASHBOARD_FILE}")


if __name__ == "__main__":
    main()