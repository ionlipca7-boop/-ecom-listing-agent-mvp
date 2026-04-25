import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MANIFEST_FILE = Path("final_publish_manifest_v1.json")
OUTPUT_FILE = Path("real_publish_approval_v1.json")


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

    manifest_ok, manifest_payload, manifest_error = _safe_read_json(MANIFEST_FILE)

    last_package: str | None = None
    publish_mode: str | None = None

    if not manifest_ok or not isinstance(manifest_payload, dict):
        reasons.append(f"final_publish_manifest_v1.json:{manifest_error or 'invalid_root'}")
    else:
        manifest_package = manifest_payload.get("last_package")
        if isinstance(manifest_package, str) and manifest_package.strip():
            last_package = manifest_package.strip()

        manifest_mode = manifest_payload.get("publish_mode")
        if isinstance(manifest_mode, str) and manifest_mode.strip():
            publish_mode = manifest_mode.strip()

        if str(manifest_payload.get("manifest_status", "")).strip().upper() != "READY":
            reasons.append("final_publish_manifest_v1.json:manifest_status_not_READY")

    checks = {
        "final_publish_manifest_ready": (
            manifest_ok
            and isinstance(manifest_payload, dict)
            and str(manifest_payload.get("manifest_status", "")).strip().upper() == "READY"
        )
    }

    if not reasons:
        output_payload: dict[str, Any] = {
            "last_package": last_package,
            "approval_status": "APPROVED",
            "publish_mode": publish_mode or "REAL",
            "approved_at": _utc_now(),
            "source_files": {
                "final_publish_manifest": MANIFEST_FILE.as_posix(),
            },
            "checks": checks,
        }
    else:
        output_payload = {
            "last_package": last_package,
            "approval_status": "BLOCKED",
            "publish_mode": publish_mode or "REAL",
            "reasons": reasons,
            "checked_at": _utc_now(),
            "source_files": {
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
    print(f"approval_status: {output_payload['approval_status']}")
    print(f"output_file: {OUTPUT_FILE.as_posix()}")

    return 0 if output_payload["approval_status"] == "APPROVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())