import json
from pathlib import Path

INDEX_FILE = Path("control_room_history_index.json")


def load_index():
    if not INDEX_FILE.exists():
        return []

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    elif isinstance(data, dict):
        return data.get("runs", [])
    return []


def read_run(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def is_valid(data):
    return isinstance(data, dict) and data.get("status") == "READY" and data.get("timestamp")


def main():
    print("HISTORY CLEANER V2 (SAFE MODE):\n")

    runs = load_index()

    valid = []
    removed = []

    for path in runs:
        data = read_run(path)

        if is_valid(data):
            valid.append(path)
        else:
            removed.append(path)

    print(f"kept_valid_runs: {len(valid)}")
    print(f"removed_from_index: {len(removed)}")

    # 🔥 сохраняем только валидные
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(valid, f, indent=2)

    print("\nINDEX CLEANED ✅")
    print("Old runs still exist as files (safe)")
    print("System now uses only valid runs")


if __name__ == "__main__":
    main()