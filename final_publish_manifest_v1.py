import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

CONTROL_ROOM_RUN_FILE = Path("control_room_run_v1.json")
DECISION_FILE = Path("decision_output_v1.json")
GATE_FILE = Path("real_publish_gate_v1.json")
REQUEST_FILE = Path("real_publish_request_v1.json")
OUTPUT_FILE = Path("final_publish_manifest_v1.json")


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

    run_ok, run_payload, run_error = _safe_read_json(CONTROL_ROOM_RUN_FILE)
    decision_ok, decision_payload, decision_error = _safe_read_json(DECISION_FILE)
    gate_ok, gate_payload, gate_error = _safe_read_json(GATE_FILE)
    request_ok, request_payload, request_error = _safe_read_json(REQUEST_FILE)

    last_package: str | None = None
    publish_mode: str | None = None

    if not run_ok or not isinstance(run_payload, dict):
        reasons.append(f"control_room_run_v1.json:{run_error or 'invalid_root'}")
    else:
        run_pkg = run_payload.get("last_package_detected")
        if isinstance(run_pkg, str) and run_pkg.strip():
            last_package = run_pkg.strip()
        if str(run_payload.get("final_status", "")).strip().upper() != "READY":
            reasons.append("control_room_run_v1.json:final_status_not_READY")

    if not decision_ok or not isinstance(decision_payload, dict):
        reasons.append(f"decision_output_v1.json:{decision_error or 'invalid_root'}")
    else:
        if last_package is None:
            decision_pkg = decision_payload.get("last_package")
            if isinstance(decision_pkg, str) and decision_pkg.strip():
                last_package = decision_pkg.strip()
        if str(decision_payload.get("next_action", "")).strip().upper() != "READY_FOR_REAL_PUBLISH":
            reasons.append("decision_output_v1.json:next_action_not_READY_FOR_REAL_PUBLISH")

    if not gate_ok or not isinstance(gate_payload, dict):
        reasons.append(f"real_publish_gate_v1.json:{gate_error or 'invalid_root'}")
    else:
        if last_package is None:
            gate_pkg = gate_payload.get("last_package")
            if isinstance(gate_pkg, str) and gate_pkg.strip():
                last_package = gate_pkg.strip()
        if str(gate_payload.get("gate_status", "")).strip().upper() != "OPEN":
            reasons.append("real_publish_gate_v1.json:gate_status_not_OPEN")

    if not request_ok or not isinstance(request_payload, dict):
        reasons.append(f"real_publish_request_v1.json:{request_error or 'invalid_root'}")
    else:
        if last_package is None:
            request_pkg = request_payload.get("last_package")
            if isinstance(request_pkg, str) and request_pkg.strip():
                last_package = request_pkg.strip()
        request_mode = request_payload.get("publish_mode")
        if isinstance(request_mode, str) and request_mode.strip():
            publish_mode = request_mode.strip()
        if str(request_payload.get("request_status", "")).strip().upper() != "CREATED":
            reasons.append("real_publish_request_v1.json:request_status_not_CREATED")

    checks = {
        "control_room_run_ready": (
            run_ok
            and isinstance(run_payload, dict)
            and str(run_payload.get("final_status", "")).strip().upper() == "READY"
        ),
        "decision_ready_for_real_publish": (
            decision_ok
            and isinstance(decision_payload, dict)
            and str(decision_payload.get("next_action", "")).strip().upper() == "READY_FOR_REAL_PUBLISH"
        ),
        "real_publish_gate_open": (
            gate_ok
            and isinstance(gate_payload, dict)
            and str(gate_payload.get("gate_status", "")).strip().upper() == "OPEN"
        ),
        "real_publish_request_created": (
            request_ok
            and isinstance(request_payload, dict)
            and str(request_payload.get("request_status", "")).strip().upper() == "CREATED"
        ),
    }

    source_files = {
        "control_room_run": CONTROL_ROOM_RUN_FILE.as_posix(),
        "decision_output": DECISION_FILE.as_posix(),
        "real_publish_gate": GATE_FILE.as_posix(),
        "real_publish_request": REQUEST_FILE.as_posix(),
    }

    if not reasons:
        manifest_payload: dict[str, Any] = {
            "manifest_status": "READY",
            "last_package": last_package,
            "publish_mode": publish_mode or "REAL",
            "created_at": _utc_now(),
            "source_files": source_files,
            "checks": checks,
        }
    else:
        manifest_payload = {
            "manifest_status": "BLOCKED",
            "last_package": last_package,
            "publish_mode": publish_mode or "REAL",
            "reasons": reasons,
            "checked_at": _utc_now(),
            "source_files": source_files,
            "checks": checks,
        }

    write_ok, write_result = _write_json(OUTPUT_FILE, manifest_payload)
    if not write_ok:
        print(json.dumps(manifest_payload, ensure_ascii=False, indent=2))
        print(write_result)
        return 1

    print(f"last_package: {last_package}")
    print(f"manifest_status: {manifest_payload['manifest_status']}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")

    return 0 if manifest_payload["manifest_status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())