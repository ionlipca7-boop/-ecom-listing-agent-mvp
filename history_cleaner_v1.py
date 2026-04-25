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
    print("HISTORY CLEANER:\n")

    runs = load_index()

    valid = []
    invalid = []

    for path in runs:
        data = read_run(path)
        if is_valid(data):
            valid.append(path)
        else:
            invalid.append(path)

    print(f"valid_runs: {len(valid)}")
    print(f"invalid_runs: {len(invalid)}")

    print("\nINVALID RUNS (can be removed):")
    for r in invalid:
        print(r)

    print("\nNEXT STEP:")
    print("If ok → we will clean index safely")


if __name__ == "__main__":
    main()