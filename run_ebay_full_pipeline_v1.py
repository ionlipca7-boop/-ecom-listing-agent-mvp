import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

INDEX_FILE = Path("control_room_history_index.json")
DASHBOARD_FILE = Path("control_room_dashboard_v2.json")
PUBLISH_MODE_FILE = Path("publish_mode_config_v1.json")
SANDBOX_RESULT_FILE = Path("ebay_inventory_execution_v1.json")


def run(cmd: str) -> None:
    print(f"\nRUNNING: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR: {cmd}")
        raise SystemExit(result.returncode)


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe_read_json(path: Path) -> Any | None:
    if not path.exists():
        return None

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def load_index() -> list[dict[str, Any]]:
    data = _safe_read_json(INDEX_FILE)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        runs = data.get("runs", [])
        if isinstance(runs, list):
            return runs

    return []


def save_index(runs: list[dict[str, Any]]) -> None:
    with INDEX_FILE.open("w", encoding="utf-8") as f:
        json.dump(runs, f, ensure_ascii=False, indent=2)


def read_dashboard() -> dict[str, Any]:
    data = _safe_read_json(DASHBOARD_FILE)
    if isinstance(data, dict):
        return data
    return {}


def get_publish_mode() -> str:
    data = _safe_read_json(PUBLISH_MODE_FILE)
    if not isinstance(data, dict):
        return "mock"

    mode = str(data.get("mode", "mock")).strip().lower()
    if mode in {"mock", "sandbox", "real"}:
        return mode

    return "mock"


def get_final_verdict(mode: str) -> tuple[str, str]:
    if mode == "mock":
        return "MOCK_READY", "Mock pipeline completed successfully"

    if mode == "sandbox":
        data = _safe_read_json(SANDBOX_RESULT_FILE)
        if not isinstance(data, dict):
            return "SANDBOX_UNKNOWN", "Sandbox result file missing or invalid"

        sandbox_status = str(data.get("status", "UNKNOWN")).strip().upper()

        if sandbox_status == "BLOCKED":
            return "SANDBOX_BLOCKED", str(data.get("reason", "Sandbox blocked"))
        if sandbox_status == "SUCCESS":
            return "SANDBOX_READY", "Sandbox request completed successfully"
        if sandbox_status == "FAILED":
            return "SANDBOX_FAILED", str(data.get("reason", "Sandbox request failed"))
        if sandbox_status == "NOT_READY":
            return "SANDBOX_NOT_READY", str(data.get("reason", "Sandbox payload not ready"))

        return "SANDBOX_UNKNOWN", f"Unhandled sandbox status: {sandbox_status}"

    if mode == "real":
        return "REAL_API_PENDING", "Real API mode selected but real execution verdict is not integrated yet"

    return "UNKNOWN_MODE", f"Unsupported publish mode: {mode}"


def archive_run(final_status: str, final_reason: str) -> dict[str, Any]:
    runs = load_index()
    dashboard = read_dashboard()
    last_valid = dashboard.get("last_valid_run", {})

    run_record = {
        "timestamp": utc_now(),
        "status": final_status,
        "reason": final_reason,
        "package": last_valid.get("package", "UNKNOWN_PACKAGE"),
        "next_step": dashboard.get("next_step", "UNKNOWN_NEXT_STEP"),
    }

    runs.append(run_record)
    save_index(runs)
    return run_record


def main() -> int:
    print("=== EBAY FULL PIPELINE START ===")

    run("python run_control_room_dashboard_v2.py")
    run("python history_inspector_v2.py")
    run("python run_stability_guard_v1.py")

    from run_stability_guard_v1 import evaluate_stability
    state = evaluate_stability()
    print(f"\nSYSTEM STATE: {state['system_state']}")

    run("python ebay_location_prepare_v1.py")
    run("python ebay_api_prepare_inventory_v1.py")
    run("python ebay_offer_prepare_v1.py")
    run("python publish_router_v1.py")

    mode = get_publish_mode()
    final_status, final_reason = get_final_verdict(mode)

    archived = archive_run(final_status, final_reason)
    print("\nARCHIVE RUN:")
    print(json.dumps(archived, ensure_ascii=False, indent=2))

    print("\n=== PIPELINE COMPLETE ===")
    print(f"STATUS: {final_status}")
    print(f"REASON: {final_reason}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())