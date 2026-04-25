import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

STATE_FILE = Path("control_room_state_v1.json")
OUTPUT_FILE = Path("decision_output_v1.json")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe_read_json(path: Path) -> tuple[bool, Any | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return True, payload, None
    except FileNotFoundError:
        return False, None, "missing"
    except json.JSONDecodeError as exc:
        return False, None, f"invalid_json: {exc}"
    except OSError as exc:
        return False, None, f"read_error: {exc}"


def _write_json(path: Path, payload: dict[str, Any]) -> tuple[bool, str]:
    try:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return True, path.as_posix()
    except OSError as exc:
        return False, f"write_error: {exc}"


def _resolve_next_action(last_status: str | None, state_missing: bool) -> str:
    if state_missing:
        return "BOOTSTRAP_REQUIRED"

    status = (last_status or "").strip().upper()
    if status == "SUCCESS":
        return "READY_FOR_REAL_PUBLISH"
    if status == "BLOCKED":
        return "REVIEW_REQUIRED"
    return "MANUAL_CHECK_REQUIRED"


def main() -> int:
    ok, state_payload, read_error = _safe_read_json(STATE_FILE)

    if not ok:
        decision_payload = {
            "last_package": None,
            "last_status": None,
            "last_step": None,
            "next_action": _resolve_next_action(last_status=None, state_missing=True),
            "generated_at": _utc_now(),
        }
        if read_error:
            decision_payload["state_warning"] = read_error

        write_ok, write_info = _write_json(OUTPUT_FILE, decision_payload)
        if not write_ok:
            print(json.dumps(decision_payload, ensure_ascii=False, indent=2))
            print(write_info)
            return 1

        print("last_package: None")
        print("last_status: None")
        print(f"next_action: {decision_payload['next_action']}")
        print(f"output_file: {OUTPUT_FILE.as_posix()}")
        return 1

    if not isinstance(state_payload, dict):
        state_payload = {}

    last_package = state_payload.get("last_package")
    last_status = state_payload.get("last_status")
    last_step = state_payload.get("last_step")

    decision_payload = {
        "last_package": last_package,
        "last_status": last_status,
        "last_step": last_step,
        "next_action": _resolve_next_action(
            str(last_status) if last_status is not None else None,
            state_missing=False,
        ),
        "generated_at": _utc_now(),
    }

    write_ok, write_info = _write_json(OUTPUT_FILE, decision_payload)
    if not write_ok:
        print(json.dumps(decision_payload, ensure_ascii=False, indent=2))
        print(write_info)
        return 1

    print(f"last_package: {last_package}")
    print(f"last_status: {last_status}")
    print(f"next_action: {decision_payload['next_action']}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())