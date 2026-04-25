import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

CONTROL_ROOM_RUN_FILE = Path("control_room_run_v1.json")
REQUEST_FILE = Path("real_publish_request_v1.json")
MANIFEST_FILE = Path("final_publish_manifest_v1.json")
APPROVAL_FILE = Path("real_publish_approval_v1.json")
FLOW_FILE = Path("full_publish_flow_v1.json")
OUTPUT_FILE = Path("control_room_report_v1.json")


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


def _extract_last_package(*payloads: Any) -> str | None:
    for payload in payloads:
        if not isinstance(payload, dict):
            continue
        for key in ("last_package", "last_package_detected"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _extract_status(payload: Any, key: str) -> str | None:
    if not isinstance(payload, dict):
        return None
    value = payload.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def main() -> int:
    issues: list[str] = []

    run_ok, run_payload, run_error = _safe_read_json(CONTROL_ROOM_RUN_FILE)
    request_ok, request_payload, request_error = _safe_read_json(REQUEST_FILE)
    manifest_ok, manifest_payload, manifest_error = _safe_read_json(MANIFEST_FILE)
    approval_ok, approval_payload, approval_error = _safe_read_json(APPROVAL_FILE)
    flow_ok, flow_payload, flow_error = _safe_read_json(FLOW_FILE)

    if not run_ok:
        issues.append(f"control_room_run_v1.json:{run_error}")
    if not request_ok:
        issues.append(f"real_publish_request_v1.json:{request_error}")
    if not manifest_ok:
        issues.append(f"final_publish_manifest_v1.json:{manifest_error}")
    if not approval_ok:
        issues.append(f"real_publish_approval_v1.json:{approval_error}")
    if not flow_ok:
        issues.append(f"full_publish_flow_v1.json:{flow_error}")

    run_status = _extract_status(run_payload, "final_status")
    request_status = _extract_status(request_payload, "request_status")
    manifest_status = _extract_status(manifest_payload, "manifest_status")
    approval_status = _extract_status(approval_payload, "approval_status")
    flow_status = _extract_status(flow_payload, "flow_status")

    if run_ok and run_status != "READY":
        issues.append(f"control_room_run_status={run_status or 'MISSING'}")
    if request_ok and request_status != "CREATED":
        issues.append(f"real_publish_request_status={request_status or 'MISSING'}")
    if manifest_ok and manifest_status != "READY":
        issues.append(f"final_publish_manifest_status={manifest_status or 'MISSING'}")
    if approval_ok and approval_status != "APPROVED":
        issues.append(f"real_publish_approval_status={approval_status or 'MISSING'}")
    if flow_ok and flow_status != "APPROVED":
        issues.append(f"full_publish_flow_status={flow_status or 'MISSING'}")

    last_package = _extract_last_package(
        run_payload,
        request_payload,
        manifest_payload,
        approval_payload,
        flow_payload,
    )

    report_status = "OK" if not issues else "ISSUES_FOUND"

    report_payload: dict[str, Any] = {
        "checked_at": _utc_now(),
        "report_status": report_status,
        "last_package": last_package,
        "summary": {
            "control_room_run_final_status": run_status,
            "real_publish_request_status": request_status,
            "final_publish_manifest_status": manifest_status,
            "real_publish_approval_status": approval_status,
            "full_publish_flow_status": flow_status,
        },
        "source_files": {
            "control_room_run": CONTROL_ROOM_RUN_FILE.as_posix(),
            "real_publish_request": REQUEST_FILE.as_posix(),
            "final_publish_manifest": MANIFEST_FILE.as_posix(),
            "real_publish_approval": APPROVAL_FILE.as_posix(),
            "full_publish_flow": FLOW_FILE.as_posix(),
        },
        "issues": issues,
    }

    OUTPUT_FILE.write_text(
        json.dumps(report_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"last_package: {last_package}")
    print(f"report_status: {report_status}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")

    if issues:
        print("ISSUES:")
        for issue in issues:
            print(f"- {issue}")

    return 0 if report_status == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())