import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PUBLISH_PACKAGES_DIR = Path("publish_packages")
PUBLISH_INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
STATE_FILE_PATH = Path("control_room_state_v1.json")
UPLOAD_PACKAGE_DIR_NAME = "ebay_upload_package_v1"


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


def _resolve_latest_package() -> tuple[str | None, str | None]:
    ok, payload, error = _safe_read_json(PUBLISH_INDEX_PATH)
    if not ok:
        if error == "missing":
            return None, "publish_index_missing"
        return None, f"publish_index_invalid ({error})"

    if not isinstance(payload, dict):
        return None, "publish_index_invalid (root_not_object)"

    latest_package = payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package.strip():
        return None, "latest_package_missing"

    return latest_package.strip(), None


def _write_state(payload: dict[str, Any]) -> tuple[bool, str]:
    try:
        STATE_FILE_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True, STATE_FILE_PATH.as_posix()
    except OSError as exc:
        return False, f"write_error: {exc}"


def main() -> int:
    package_id, package_error = _resolve_latest_package()

    if not package_id:
        state_payload = {
            "last_package": None,
            "last_status": "BLOCKED",
            "last_step": "execution",
            "updated_at": _utc_now(),
            "source": {
                "manifest": None,
                "result": None,
            },
            "error": package_error or "package_resolution_failed",
        }
        ok, info = _write_state(state_payload)
        if not ok:
            print(json.dumps(state_payload, ensure_ascii=False, indent=2))
            print(info)
            return 1

        print("last_package: None")
        print("last_status: BLOCKED")
        print(f"state_file_path: {STATE_FILE_PATH.as_posix()}")
        return 1

    package_dir = PUBLISH_PACKAGES_DIR / package_id / UPLOAD_PACKAGE_DIR_NAME
    result_path = package_dir / "publish_result_v1.json"
    manifest_path = package_dir / "manifest.json"

    result_ok, result_payload, result_error = _safe_read_json(result_path)
    manifest_ok, manifest_payload, manifest_error = _safe_read_json(manifest_path)

    last_status = "BLOCKED"
    if result_ok and isinstance(result_payload, dict):
        last_status = str(result_payload.get("status", "BLOCKED"))
    elif manifest_ok and isinstance(manifest_payload, dict):
        last_status = str(manifest_payload.get("status", "BLOCKED"))

    state_payload: dict[str, Any] = {
        "last_package": package_id,
        "last_status": last_status,
        "last_step": "execution",
        "updated_at": _utc_now(),
        "source": {
            "manifest": manifest_path.as_posix(),
            "result": result_path.as_posix(),
        },
    }

    if package_error:
        state_payload["package_warning"] = package_error
    if not result_ok:
        state_payload["result_warning"] = result_error
    if not manifest_ok:
        state_payload["manifest_warning"] = manifest_error

    ok, info = _write_state(state_payload)
    if not ok:
        print(json.dumps(state_payload, ensure_ascii=False, indent=2))
        print(info)
        return 1

    print(f"last_package: {package_id}")
    print(f"last_status: {last_status}")
    print(f"state_file_path: {STATE_FILE_PATH.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())