from pathlib import Path
from typing import Any

from history_inspector_v2 import inspect_history

HISTORY_INDEX_PATH = Path("control_room_history_index.json")


def evaluate_stability(path: Path = HISTORY_INDEX_PATH) -> dict[str, Any]:
    summary = inspect_history(path)
    valid_runs = summary["valid_runs"]
    system_state = "STABLE" if valid_runs >= 3 else "UNSTABLE"
    return {
        "valid_runs": valid_runs,
        "system_state": system_state,
    }


def main() -> int:
    result = evaluate_stability()
    print("RUN STABILITY GUARD V1")
    print(f"valid_runs: {result['valid_runs']}")
    print(f"system_state: {result['system_state']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())