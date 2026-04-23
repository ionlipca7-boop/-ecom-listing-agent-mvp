import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ACTION_FILE = Path("real_ebay_upload_action_v1.json")
OUTPUT_FILE = Path("real_ebay_upload_execution_v1.json")


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
    reasons: list[str] = []

    action_ok, action_payload, action_error = _safe_read_json(ACTION_FILE)

    last_package: str | None = None
    publish_mode: str | None = None
    action_type: str | None = None

    if not action_ok or not isinstance(action_payload, dict):
        reasons.append(f"real_ebay_upload_action_v1.json:{action_error or 'invalid_root'}")
    else:
        package_value = action_payload.get("last_package")
        if isinstance(package_value, str) and package_value.strip():
            last_package = package_value.strip()

        publish_mode_value = action_payload.get("publish_mode")
        if isinstance(publish_mode_value, str) and publish_mode_value.strip():
            publish_mode = publish_mode_value.strip()

        action_type_value = action_payload.get("action_type")
        if isinstance(action_type_value, str) and action_type_value.strip():
            action_type = action_type_value.strip()

        if str(action_payload.get("action_status", "")).strip().upper() != "READY_TO_EXECUTE":
            reasons.append("real_ebay_upload_action_v1.json:action_status_not_READY_TO_EXECUTE")

    checks = {
        "action_is_ready_to_execute": (
            action_ok
            and isinstance(action_payload, dict)
            and str(action_payload.get("action_status", "")).strip().upper() == "READY_TO_EXECUTE"
        )
    }

    if not reasons:
        output_payload: dict[str, Any] = {
            "last_package": last_package,
            "execution_status": "MANUAL_UPLOAD_REQUIRED",
            "publish_mode": publish_mode or "REAL",
            "action_type": action_type or "REAL_EBAY_UPLOAD",
            "executed_at": _utc_now(),
            "execution_mode": "MANUAL_HANDOFF",
            "next_step": "UPLOAD_TO_EBAY_MANUALLY_OR_CONNECT_REAL_API",
            "source_files": {
                "real_ebay_upload_action": ACTION_FILE.as_posix(),
            },
            "checks": checks,
        }
    else:
        output_payload = {
            "last_package": last_package,
            "execution_status": "BLOCKED",
            "publish_mode": publish_mode or "REAL",
            "action_type": action_type or "REAL_EBAY_UPLOAD",
            "reasons": reasons,
            "checked_at": _utc_now(),
            "execution_mode": "MANUAL_HANDOFF",
            "source_files": {
                "real_ebay_upload_action": ACTION_FILE.as_posix(),
            },
            "checks": checks,
        }

    write_ok, write_result = _write_json(OUTPUT_FILE, output_payload)
    if not write_ok:
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
        print(write_result)
        return 1

    print(f"last_package: {last_package}")
    print(f"execution_status: {output_payload['execution_status']}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")

    return 0 if output_payload["execution_status"] == "MANUAL_UPLOAD_REQUIRED" else 1


if __name__ == "__main__":
    raise SystemExit(main())