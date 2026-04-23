import json
from pathlib import Path

INDEX_FILE = Path("control_room_history_index.json")


def main():
    if not INDEX_FILE.exists():
        print("ERROR: index file not found")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    runs = data.get("runs", [])

    if not runs:
        print("NO RUNS FOUND")
        return

    total = len(runs)
    ready = [r for r in runs if r.get("dashboard_status") == "READY"]
    not_ready = total - len(ready)

    last_run = runs[-1]

    print("CONTROL ROOM INSPECTOR:\n")

    print(f"total_runs: {total}")
    print(f"ready_runs: {len(ready)}")
    print(f"not_ready_runs: {not_ready}\n")

    print("LAST RUN:")
    print(f"file: {last_run.get('file')}")
    print(f"status: {last_run.get('dashboard_status')}")
    print(f"package: {last_run.get('last_package')}")
    print(f"next_step: {last_run.get('next_step')}\n")

    if last_run.get("dashboard_status") == "READY":
        print("RECOMMENDATION: PROCEED TO EBAY UPLOAD OR API INTEGRATION")
    else:
        print("RECOMMENDATION: INVESTIGATE FAILED RUN")


if __name__ == "__main__":
    main()