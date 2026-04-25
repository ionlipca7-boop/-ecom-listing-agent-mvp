import json
from datetime import datetime, UTC
from pathlib import Path

DASHBOARD_FILE = Path("control_room_dashboard_v1.json")
OUTPUT_FILE = Path("upload_execution_v2.json")


def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def main():
    if not DASHBOARD_FILE.exists():
        print("ERROR: dashboard not found")
        return

    with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
        dashboard = json.load(f)

    decision = dashboard.get("decision")

    if decision != "SAFE_TO_CONNECT_EBAY_API":
        result = {
            "execution_status": "BLOCKED",
            "reason": "SYSTEM_NOT_READY",
            "checked_at": utc_now()
        }
    else:
        result = {
            "execution_status": "SIMULATED_UPLOAD_SUCCESS",
            "mode": "SIMULATION",
            "package": dashboard.get("last_package"),
            "checked_at": utc_now()
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("UPLOAD EXECUTOR V2:")
    print(f"status: {result['execution_status']}")
    print(f"mode: {result.get('mode', 'N/A')}")
    print(f"output_file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()