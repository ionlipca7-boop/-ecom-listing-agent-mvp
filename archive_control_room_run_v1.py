import json
from datetime import datetime, UTC
from pathlib import Path

DASHBOARD_FILE = Path("control_room_dashboard_v1.json")
HISTORY_DIR = Path("control_room_history")


def utc_now():
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def main():
    if not DASHBOARD_FILE.exists():
        print("ERROR: dashboard file not found")
        return

    HISTORY_DIR.mkdir(exist_ok=True)

    with open(DASHBOARD_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    timestamp = utc_now()
    output_file = HISTORY_DIR / f"run_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("ARCHIVE CREATED:")
    print(f"file: {output_file}")


if __name__ == "__main__":
    main()