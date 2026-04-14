import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"

KEY_FILES = [
    Path("build_dedup_ebay_feed.py"),
    Path("build_final_ebay_feed.py"),
    Path("audit_final_ebay_feed.py"),
    Path("build_publish_ready_summary.py"),
]

PACKAGE_FILES = [
    "ebay_feed.csv",
    "ebay_feed_dedup.csv",
    "ebay_feed_final.csv",
    "ebay_feed_final_audit.json",
    "publish_ready_summary.json",
]


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_duplicate_titles_count(audit_payload) -> int | None:
    if not isinstance(audit_payload, dict):
        return None

    direct = audit_payload.get("duplicate_titles_count")
    if isinstance(direct, int):
        return direct

    duplicate_titles = audit_payload.get("duplicate_titles")
    if isinstance(duplicate_titles, list):
        return len(duplicate_titles)

    return None


def _extract_total_final_feed_items(audit_payload, summary_payload) -> int | None:
    if isinstance(summary_payload, dict):
        value = summary_payload.get("total_final_feed_items")
        if isinstance(value, int):
            return value

    if isinstance(audit_payload, dict):
        value = audit_payload.get("total_items")
        if isinstance(value, int):
            return value

    return None


def main() -> int:
    missing_files: list[str] = []
    broken_steps: list[str] = []

    for path in KEY_FILES:
        if not path.exists():
            missing_files.append(path.as_posix())

    package_id = None
    package_dir = None

    if not INDEX_PATH.exists():
        missing_files.append(INDEX_PATH.as_posix())
        broken_steps.append("latest_package_not_found")
    else:
        try:
            index_payload = _load_json(INDEX_PATH)
            latest_package = index_payload.get("latest_package") if isinstance(index_payload, dict) else None
            if isinstance(latest_package, str) and latest_package:
                package_id = latest_package
                package_dir = PUBLISH_PACKAGES_DIR / latest_package
            else:
                broken_steps.append("latest_package_not_found")
        except (OSError, json.JSONDecodeError):
            broken_steps.append("latest_package_not_found")

    audit_payload = None
    summary_payload = None

    if package_dir is not None:
        for file_name in PACKAGE_FILES:
            path = package_dir / file_name
            if not path.exists():
                missing_files.append(path.as_posix())

        audit_path = package_dir / "ebay_feed_final_audit.json"
        summary_path = package_dir / "publish_ready_summary.json"

        if audit_path.exists():
            try:
                audit_payload = _load_json(audit_path)
            except (OSError, json.JSONDecodeError):
                broken_steps.append("audit_json_invalid")

        if summary_path.exists():
            try:
                summary_payload = _load_json(summary_path)
            except (OSError, json.JSONDecodeError):
                broken_steps.append("summary_json_invalid")

    total_final_feed_items = _extract_total_final_feed_items(audit_payload, summary_payload)
    if total_final_feed_items is None:
        broken_steps.append("total_final_feed_items_unavailable")
    elif total_final_feed_items <= 0:
        broken_steps.append("total_final_feed_items_not_positive")

    duplicate_titles_count = _extract_duplicate_titles_count(audit_payload)
    if duplicate_titles_count is None:
        broken_steps.append("duplicate_titles_count_unavailable")
    elif duplicate_titles_count != 0:
        broken_steps.append("duplicate_titles_count_not_zero")

    # De-duplicate while keeping order
    broken_steps = list(dict.fromkeys(broken_steps))
    missing_files = list(dict.fromkeys(missing_files))

    has_key_file_errors = any(path in {p.as_posix() for p in KEY_FILES} or path == INDEX_PATH.as_posix() for path in missing_files)
    if has_key_file_errors or "latest_package_not_found" in broken_steps:
        project_status = "ERROR"
    elif missing_files or broken_steps:
        project_status = "WARNING"
    else:
        project_status = "OK"

    result = {
        "project_status": project_status,
        "missing_files": missing_files,
        "broken_steps": broken_steps,
        "package_id": package_id,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
