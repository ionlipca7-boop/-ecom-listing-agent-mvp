import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"


def _load_json(path: Path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"failed_to_read_json: {path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"invalid_json_object: {path.as_posix()}")

    return payload


def _as_int(value) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    return 0


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


def _pick_first(payload: dict, *keys):
    for key in keys:
        if key in payload:
            return payload.get(key)
    return None


def _read_status() -> dict:
    index_payload = _load_json(INDEX_PATH)

    latest_package = index_payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        raise ValueError("latest_package_not_found")

    package_dir = PUBLISH_PACKAGES_DIR / latest_package
    summary_payload = _load_json(package_dir / "publish_ready_summary.json")
    audit_payload = _load_json(package_dir / "ebay_feed_final_audit.json")

    package_id = _pick_first(summary_payload, "package_id")
    if not isinstance(package_id, str) or not package_id:
        package_id = latest_package

    final_publish_ready = _as_bool(
        _pick_first(summary_payload, "final_publish_ready", "publish_ready")
    )

    total_manifest_items = _as_int(_pick_first(summary_payload, "total_manifest_items"))
    total_final_feed_items = _as_int(
        _pick_first(summary_payload, "total_final_feed_items")
    )

    duplicate_titles_count = _as_int(
        _pick_first(audit_payload, "duplicate_titles_count")
    )

    project_status = (
        "OK"
        if final_publish_ready is True and duplicate_titles_count == 0
        else "WARNING"
    )

    return {
        "package_id": package_id,
        "final_publish_ready": final_publish_ready,
        "total_manifest_items": total_manifest_items,
        "total_final_feed_items": total_final_feed_items,
        "duplicate_titles_count": duplicate_titles_count,
        "project_status": project_status,
    }


def main() -> int:
    try:
        status = _read_status()
    except ValueError as exc:
        print(f"error: {exc}")
        return 1

    print(f"package_id: {status['package_id']}")
    print(f"final_publish_ready: {status['final_publish_ready']}")
    print(f"total_manifest_items: {status['total_manifest_items']}")
    print(f"total_final_feed_items: {status['total_final_feed_items']}")
    print(f"duplicate_titles_count: {status['duplicate_titles_count']}")
    print(f"project_status: {status['project_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
