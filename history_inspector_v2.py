import json
from pathlib import Path
from typing import Any

INDEX_FILE = Path("control_room_history_index.json")

MEANINGFUL_STATUSES = {
    "READY",
    "SANDBOX_BLOCKED",
    "SANDBOX_READY",
    "SANDBOX_FAILED",
    "SANDBOX_NOT_READY",
    "REAL_API_PENDING",
}


def _load_index(path: Path = INDEX_FILE) -> list[Any]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        runs = data.get("runs", [])
        if isinstance(runs, list):
            return runs

    return []


def _read_json_file(path_str: str) -> dict[str, Any]:
    try:
        with open(path_str, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def _normalize_run(item: Any) -> dict[str, Any]:
    if isinstance(item, str):
        data = _read_json_file(item)
        return {
            "file": item,
            "timestamp": data.get("timestamp") or data.get("checked_at"),
            "status": data.get("status") or data.get("dashboard_status"),
            "package": data.get("package") or data.get("last_package"),
            "next_step": data.get("next_step"),
            "reason": data.get("reason"),
        }

    if isinstance(item, dict):
        if "file" in item and ("status" not in item or "timestamp" not in item):
            data = _read_json_file(item.get("file", ""))
            return {
                "file": item.get("file"),
                "timestamp": item.get("timestamp") or item.get("checked_at") or data.get("timestamp") or data.get("checked_at"),
                "status": item.get("status") or item.get("dashboard_status") or data.get("status") or data.get("dashboard_status"),
                "package": item.get("package") or item.get("last_package") or data.get("package") or data.get("last_package"),
                "next_step": item.get("next_step") or data.get("next_step"),
                "reason": item.get("reason") or data.get("reason"),
            }

        return {
            "file": item.get("file"),
            "timestamp": item.get("timestamp") or item.get("checked_at"),
            "status": item.get("status") or item.get("dashboard_status"),
            "package": item.get("package") or item.get("last_package"),
            "next_step": item.get("next_step"),
            "reason": item.get("reason"),
        }

    return {}


def inspect_history(path: Path = INDEX_FILE) -> dict[str, Any]:
    raw_runs = _load_index(path)
    normalized_runs = [_normalize_run(item) for item in raw_runs]

    ready_runs = [
        run for run in normalized_runs
        if run.get("status") == "READY" and run.get("timestamp")
    ]

    meaningful_runs = [
        run for run in normalized_runs
        if run.get("status") in MEANINGFUL_STATUSES and run.get("timestamp")
    ]

    invalid_runs = [
        run for run in normalized_runs
        if not (run.get("status") in MEANINGFUL_STATUSES and run.get("timestamp"))
    ]

    last_ready_run = ready_runs[-1] if ready_runs else {}
    last_meaningful_run = meaningful_runs[-1] if meaningful_runs else {}

    return {
        "total_runs": len(normalized_runs),
        "ready_runs": len(ready_runs),
        "meaningful_runs": len(meaningful_runs),
        "invalid_runs": len(invalid_runs),
        "last_ready_run": last_ready_run,
        "last_meaningful_run": last_meaningful_run,
    }


def _print_run_block(title: str, run: dict[str, Any]) -> None:
    print(f"\n{title}:")
    if run:
        print(f"file: {run.get('file')}")
        print(f"status: {run.get('status')}")
        print(f"timestamp: {run.get('timestamp')}")
        print(f"package: {run.get('package')}")
        print(f"next_step: {run.get('next_step')}")
        print(f"reason: {run.get('reason')}")
    else:
        print("file: None")
        print("status: None")
        print("timestamp: None")
        print("package: None")
        print("next_step: None")
        print("reason: None")


def main() -> int:
    result = inspect_history()

    print("CONTROL ROOM INSPECTOR V2:\n")
    print(f"total_runs: {result['total_runs']}")
    print(f"ready_runs: {result['ready_runs']}")
    print(f"meaningful_runs: {result['meaningful_runs']}")
    print(f"invalid_runs: {result['invalid_runs']}")

    _print_run_block("LAST READY RUN", result["last_ready_run"])
    _print_run_block("LAST MEANINGFUL RUN", result["last_meaningful_run"])

    if result["meaningful_runs"] >= 3:
        print("\nRECOMMENDATION: PROCEED TO EBAY UPLOAD OR API INTEGRATION")
    else:
        print("\nRECOMMENDATION: WAIT AND MONITOR")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())