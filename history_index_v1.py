import json
from pathlib import Path

HISTORY_DIR = Path("control_room_history")
OUTPUT_FILE = Path("control_room_history_index.json")


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def main():
    if not HISTORY_DIR.exists():
        print("ERROR: history folder not found")
        return

    records = []

    for file in sorted(HISTORY_DIR.glob("run_*.json")):
        data = load_json(file)
        if not data:
            continue

        record = {
            "file": str(file),
            "checked_at": data.get("checked_at"),
            "dashboard_status": data.get("dashboard_status"),
            "last_package": data.get("last_package"),
            "next_step": data.get("next_step"),
        }

        records.append(record)

    output = {
        "total_runs": len(records),
        "runs": records
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("HISTORY INDEX CREATED:")
    print(f"runs: {len(records)}")
    print(f"file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()