import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_item_count(payload) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        items = payload.get("items")
        if isinstance(items, list):
            return len(items)
    return 0


def _extract_final_feed_items_count(audit_payload) -> int:
    if not isinstance(audit_payload, dict):
        return 0

    total_items = audit_payload.get("total_items")
    if isinstance(total_items, int):
        return total_items

    # Fallback for legacy/non-standard shapes to keep backward compatibility.
    return _extract_item_count(audit_payload)


def _extract_duplicate_titles_count(audit_payload) -> int:
    if not isinstance(audit_payload, dict):
        return 0

    direct = audit_payload.get("duplicate_titles_count")
    if isinstance(direct, int):
        return direct

    duplicate_titles = audit_payload.get("duplicate_titles")
    if isinstance(duplicate_titles, list):
        return len(duplicate_titles)

    return 0


def main() -> int:
    if not INDEX_PATH.exists():
        print(f"error: missing index file: {INDEX_PATH.as_posix()}")
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
    manifest_path = package_dir / "manifest.json"
    audit_path = package_dir / "ebay_feed_final_audit.json"

    if not manifest_path.exists():
        print(f"error: missing manifest file: {manifest_path.as_posix()}")
        return 1
    if not audit_path.exists():
        print(f"error: missing final audit file: {audit_path.as_posix()}")
        return 1

    manifest_payload = _load_json(manifest_path)
    audit_payload = _load_json(audit_path)

    total_manifest_items = _extract_item_count(manifest_payload)
    total_final_feed_items = _extract_final_feed_items_count(audit_payload)
    duplicate_titles_count = _extract_duplicate_titles_count(audit_payload)
    publish_ready = total_final_feed_items > 0 and duplicate_titles_count == 0

    summary_payload = {
        "package_id": latest_package,
        "total_manifest_items": total_manifest_items,
        "total_final_feed_items": total_final_feed_items,
        "duplicate_titles_count": duplicate_titles_count,
        "publish_ready": publish_ready,
    }

    output_path = package_dir / "publish_ready_summary.json"
    output_path.write_text(json.dumps(summary_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"package_id: {summary_payload['package_id']}")
    print(f"total_manifest_items: {summary_payload['total_manifest_items']}")
    print(f"total_final_feed_items: {summary_payload['total_final_feed_items']}")
    print(f"duplicate_titles_count: {summary_payload['duplicate_titles_count']}")
    print(f"publish_ready: {summary_payload['publish_ready']}")
    print(f"output_file: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
