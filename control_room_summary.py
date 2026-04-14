import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _as_int(value) -> int:
    return value if isinstance(value, int) else 0


def _as_bool(value) -> bool:
    return value if isinstance(value, bool) else False


def main() -> int:
    if not INDEX_PATH.exists():
        print("error: missing publish_packages/publish_index.json")
        return 1

    index_payload = _load_json(INDEX_PATH)
    if not isinstance(index_payload, dict):
        print("error: invalid publish_index.json format")
        return 1

    latest_package = index_payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        print("error: latest_package is missing in publish_index.json")
        return 1

    package_dir = PUBLISH_PACKAGES_DIR / latest_package
    summary_path = package_dir / "publish_ready_summary.json"
    audit_path = package_dir / "ebay_feed_final_audit.json"

    if not summary_path.exists():
        print(f"error: missing {summary_path.as_posix()}")
        return 1
    if not audit_path.exists():
        print(f"error: missing {audit_path.as_posix()}")
        return 1

    summary_payload = _load_json(summary_path)
    audit_payload = _load_json(audit_path)

    publish_ready = _as_bool(summary_payload.get("publish_ready")) if isinstance(summary_payload, dict) else False
    items = _as_int(summary_payload.get("total_final_feed_items")) if isinstance(summary_payload, dict) else 0
    duplicates = _as_int(audit_payload.get("duplicate_titles_count")) if isinstance(audit_payload, dict) else 0
    status = "READY" if publish_ready and duplicates == 0 else "CHECK"

    print(f"package_id: {latest_package}")
    print(f"ready: {publish_ready}")
    print(f"items: {items}")
    print(f"duplicates: {duplicates}")
    print(f"status: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
