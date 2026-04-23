import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

APPROVAL_FILE = Path("real_publish_approval_v1.json")
MANIFEST_FILE = Path("final_publish_manifest_v1.json")
OUTPUT_FILE = Path("real_ebay_upload_action_v1.json")


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

    approval_ok, approval_payload, approval_error = _safe_read_json(APPROVAL_FILE)
    manifest_ok, manifest_payload, manifest_error = _safe_read_json(MANIFEST_FILE)

    last_package: str | None = None
    publish_mode: str | None = None

    if not approval_ok or not isinstance(approval_payload, dict):
        reasons.append(f"real_publish_approval_v1.json:{approval_error or 'invalid_root'}")
    else:
        approval_package = approval_payload.get("last_package")
        if isinstance(approval_package, str) and approval_package.strip():
            last_package = approval_package.strip()

        approval_mode = approval_payload.get("publish_mode")
        if isinstance(approval_mode, str) and approval_mode.strip():
            publish_mode = approval_mode.strip()

        if str(approval_payload.get("approval_status", "")).strip().upper() != "APPROVED":
            reasons.append("real_publish_approval_v1.json:approval_status_not_APPROVED")

    if not manifest_ok or not isinstance(manifest_payload, dict):
        reasons.append(f"final_publish_manifest_v1.json:{manifest_error or 'invalid_root'}")
    else:
        if last_package is None:
            manifest_package = manifest_payload.get("last_package")
            if isinstance(manifest_package, str) and manifest_package.strip():
                last_package = manifest_package.strip()

        if publish_mode is None:
            manifest_mode = manifest_payload.get("publish_mode")
            if isinstance(manifest_mode, str) and manifest_mode.strip():
                publish_mode = manifest_mode.strip()

        if str(manifest_payload.get("manifest_status", "")).strip().upper() != "READY":
            reasons.append("final_publish_manifest_v1.json:manifest_status_not_READY")

    checks = {
        "approval_is_approved": (
            approval_ok
            and isinstance(approval_payload, dict)
            and str(approval_payload.get("approval_status", "")).strip().upper() == "APPROVED"
        ),
        "manifest_is_ready": (
            manifest_ok
            and isinstance(manifest_payload, dict)
            and str(manifest_payload.get("manifest_status", "")).strip().upper() == "READY"
        ),
    }

    if not reasons:
        output_payload: dict[str, Any] = {
            "last_package": last_package,
            "action_status": "READY_TO_EXECUTE",
            "publish_mode": publish_mode or "REAL",
            "action_type": "REAL_EBAY_UPLOAD",
            "prepared_at": _utc_now(),
            "source_files": {
                "real_publish_approval": APPROVAL_FILE.as_posix(),
                "final_publish_manifest": MANIFEST_FILE.as_posix(),
            },
            "checks": checks,
        }
    else:
        output_payload = {
            "last_package": last_package,
            "action_status": "BLOCKED",
            "publish_mode": publish_mode or "REAL",
            "action_type": "REAL_EBAY_UPLOAD",
            "reasons": reasons,
            "checked_at": _utc_now(),
            "source_files": {
                "real_publish_approval": APPROVAL_FILE.as_posix(),
                "final_publish_manifest": MANIFEST_FILE.as_posix(),
            },
            "checks": checks,
        }

    write_ok, write_result = _write_json(OUTPUT_FILE, output_payload)
    if not write_ok:
        print(json.dumps(output_payload, ensure_ascii=False, indent=2))
        print(write_result)
        return 1

    print(f"last_package: {last_package}")
    print(f"action_status: {output_payload['action_status']}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")

    return 0 if output_payload["action_status"] == "READY_TO_EXECUTE" else 1


if __name__ == "__main__":
    raise SystemExit(main())