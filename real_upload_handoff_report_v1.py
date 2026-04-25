import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

APPROVAL_FILE = Path("real_publish_approval_v1.json")
ACTION_FILE = Path("real_ebay_upload_action_v1.json")
EXECUTION_FILE = Path("real_ebay_upload_execution_v1.json")
MANIFEST_FILE = Path("final_publish_manifest_v1.json")
REPORT_FILE = Path("control_room_report_v1.json")
OUTPUT_FILE = Path("real_upload_handoff_report_v1.json")


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


def _extract_str(payload: Any, key: str) -> str | None:
    if not isinstance(payload, dict):
        return None
    value = payload.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def main() -> int:
    reasons: list[str] = []

    approval_ok, approval_payload, approval_error = _safe_read_json(APPROVAL_FILE)
    action_ok, action_payload, action_error = _safe_read_json(ACTION_FILE)
    execution_ok, execution_payload, execution_error = _safe_read_json(EXECUTION_FILE)
    manifest_ok, manifest_payload, manifest_error = _safe_read_json(MANIFEST_FILE)
    report_ok, report_payload, report_error = _safe_read_json(REPORT_FILE)

    if not approval_ok or not isinstance(approval_payload, dict):
        reasons.append(f"real_publish_approval_v1.json:{approval_error or 'invalid_root'}")
    if not action_ok or not isinstance(action_payload, dict):
        reasons.append(f"real_ebay_upload_action_v1.json:{action_error or 'invalid_root'}")
    if not execution_ok or not isinstance(execution_payload, dict):
        reasons.append(f"real_ebay_upload_execution_v1.json:{execution_error or 'invalid_root'}")
    if not manifest_ok or not isinstance(manifest_payload, dict):
        reasons.append(f"final_publish_manifest_v1.json:{manifest_error or 'invalid_root'}")
    if not report_ok or not isinstance(report_payload, dict):
        reasons.append(f"control_room_report_v1.json:{report_error or 'invalid_root'}")

    last_package = (
        _extract_str(execution_payload, "last_package")
        or _extract_str(action_payload, "last_package")
        or _extract_str(approval_payload, "last_package")
        or _extract_str(manifest_payload, "last_package")
    )

    publish_mode = (
        _extract_str(execution_payload, "publish_mode")
        or _extract_str(action_payload, "publish_mode")
        or _extract_str(approval_payload, "publish_mode")
        or _extract_str(manifest_payload, "publish_mode")
        or "REAL"
    )

    approval_status = _extract_str(approval_payload, "approval_status")
    action_status = _extract_str(action_payload, "action_status")
    execution_status = _extract_str(execution_payload, "execution_status")
    manifest_status = _extract_str(manifest_payload, "manifest_status")
    report_status = _extract_str(report_payload, "report_status")
    next_step = _extract_str(execution_payload, "next_step")

    if approval_ok and approval_status != "APPROVED":
        reasons.append(f"approval_status={approval_status or 'MISSING'}")
    if action_ok and action_status != "READY_TO_EXECUTE":
        reasons.append(f"action_status={action_status or 'MISSING'}")
    if execution_ok and execution_status != "MANUAL_UPLOAD_REQUIRED":
        reasons.append(f"execution_status={execution_status or 'MISSING'}")
    if manifest_ok and manifest_status != "READY":
        reasons.append(f"manifest_status={manifest_status or 'MISSING'}")
    if report_ok and report_status != "OK":
        reasons.append(f"report_status={report_status or 'MISSING'}")

    checks = {
        "approval_is_approved": approval_ok and approval_status == "APPROVED",
        "action_is_ready_to_execute": action_ok and action_status == "READY_TO_EXECUTE",
        "execution_requires_manual_upload": execution_ok and execution_status == "MANUAL_UPLOAD_REQUIRED",
        "manifest_is_ready": manifest_ok and manifest_status == "READY",
        "control_room_report_is_ok": report_ok and report_status == "OK",
    }

    if not reasons:
        output_payload: dict[str, Any] = {
            "handoff_status": "READY_FOR_MANUAL_UPLOAD",
            "last_package": last_package,
            "publish_mode": publish_mode,
            "prepared_at": _utc_now(),
            "next_step": next_step or "UPLOAD_TO_EBAY_MANUALLY_OR_CONNECT_REAL_API",
            "summary": {
                "approval_status": approval_status,
                "action_status": action_status,
                "execution_status": execution_status,
                "manifest_status": manifest_status,
                "report_status": report_status,
            },
            "source_files": {
                "real_publish_approval": APPROVAL_FILE.as_posix(),
                "real_ebay_upload_action": ACTION_FILE.as_posix(),
                "real_ebay_upload_execution": EXECUTION_FILE.as_posix(),
                "final_publish_manifest": MANIFEST_FILE.as_posix(),
                "control_room_report": REPORT_FILE.as_posix(),
            },
            "checks": checks,
        }
    else:
        output_payload = {
            "handoff_status": "BLOCKED",
            "last_package": last_package,
            "publish_mode": publish_mode,
            "checked_at": _utc_now(),
            "next_step": next_step or "FIX_BLOCKERS_FIRST",
            "summary": {
                "approval_status": approval_status,
                "action_status": action_status,
                "execution_status": execution_status,
                "manifest_status": manifest_status,
                "report_status": report_status,
            },
            "source_files": {
                "real_publish_approval": APPROVAL_FILE.as_posix(),
                "real_ebay_upload_action": ACTION_FILE.as_posix(),
                "real_ebay_upload_execution": EXECUTION_FILE.as_posix(),
                "final_publish_manifest": MANIFEST_FILE.as_posix(),
                "control_room_report": REPORT_FILE.as_posix(),
            },
            "checks": checks,
            "reasons": reasons,
        }

    write_ok, write_result = _write_json(OUTPUT_FILE, output_payload)
    if not write_ok:
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
        print(write_result)
        return 1

    print(f"last_package: {last_package}")
    print(f"handoff_status: {output_payload['handoff_status']}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")

    return 0 if output_payload["handoff_status"] == "READY_FOR_MANUAL_UPLOAD" else 1


if __name__ == "__main__":
    raise SystemExit(main())