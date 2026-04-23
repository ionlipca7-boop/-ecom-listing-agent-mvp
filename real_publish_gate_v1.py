import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

DECISION_FILE = Path("decision_output_v1.json")
OUTPUT_FILE = Path("real_publish_gate_v1.json")


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


def main() -> int:
    ok, payload, read_error = _safe_read_json(DECISION_FILE)

    if not ok or not isinstance(payload, dict):
        output_payload = {
            "last_package": None,
            "last_status": None,
            "next_action": None,
            "gate_status": "BLOCKED",
            "checked_at": _utc_now(),
        }
        if read_error:
            output_payload["decision_warning"] = read_error
    else:
        last_package = payload.get("last_package")
        last_status = payload.get("last_status")
        next_action = payload.get("next_action")

        gate_status = "OPEN" if str(next_action) == "READY_FOR_REAL_PUBLISH" else "BLOCKED"
        output_payload = {
            "last_package": last_package,
            "last_status": last_status,
            "next_action": next_action,
            "gate_status": gate_status,
            "checked_at": _utc_now(),
        }

    write_ok, write_info = _write_json(OUTPUT_FILE, output_payload)
    if not write_ok:
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
        print(write_info)
        return 1

    print(f"last_package: {output_payload.get('last_package')}")
    print(f"next_action: {output_payload.get('next_action')}")
    print(f"gate_status: {output_payload.get('gate_status')}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")
    return 0 if output_payload.get("gate_status") == "OPEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())