import json
from pathlib import Path

INDEX_FILE = Path("control_room_history_index.json")
OUTPUT_FILE = Path("decision_memory_v1.json")


def main():
    if not INDEX_FILE.exists():
        print("ERROR: history index not found")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    runs = data.get("runs", [])

    total = len(runs)
    ready_runs = [r for r in runs if r.get("dashboard_status") == "READY"]

    consecutive_ready = 0

    for r in reversed(runs):
        if r.get("dashboard_status") == "READY":
            consecutive_ready += 1
        else:
            break

    if consecutive_ready >= 3:
        system_state = "STABLE"
        decision = "SAFE_TO_CONNECT_EBAY_API"
    else:
        system_state = "UNSTABLE"
        decision = "WAIT_AND_MONITOR"

    output = {
        "total_runs": total,
        "ready_runs": len(ready_runs),
        "consecutive_ready": consecutive_ready,
        "system_state": system_state,
        "decision": decision
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("DECISION MEMORY:")
    print(f"system_state: {system_state}")
    print(f"decision: {decision}")
    print(f"consecutive_ready: {consecutive_ready}")
    print(f"output_file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()