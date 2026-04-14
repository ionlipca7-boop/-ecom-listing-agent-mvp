import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
FINAL_FEED_NAME = "ebay_feed_final.csv"
AUDIT_FILE_NAME = "ebay_feed_final_audit.json"


def _load_json(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"failed_to_read_json: {path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"invalid_json_object: {path.as_posix()}")

    return payload


def _resolve_latest_package(index_payload: dict) -> str:
    latest_package = index_payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        raise ValueError("latest_package_not_found")
    return latest_package


def _read_feed_rows(feed_path: Path) -> list[dict]:
    try:
        with feed_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except OSError as exc:
        raise ValueError(f"failed_to_read_csv: {feed_path.as_posix()}") from exc


def _normalize_title(value: str | None) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _build_report(package_id: str, rows: list[dict], output_file: Path) -> dict:
    normalized_titles = [_normalize_title(row.get("title")) for row in rows]
    non_empty_titles = [title for title in normalized_titles if title]

    total_items = len(rows)
    unique_titles_count = len(set(non_empty_titles))
    duplicate_titles_count = total_items - unique_titles_count

    return {
        "package_id": package_id,
        "total_items": total_items,
        "unique_titles_count": unique_titles_count,
        "duplicate_titles_count": duplicate_titles_count,
        "output_file": output_file.as_posix(),
    }


def _write_audit(path: Path, report: dict) -> None:
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _print_report(report: dict) -> None:
    print(f"package_id: {report['package_id']}")
    print(f"total_items: {report['total_items']}")
    print(f"unique_titles_count: {report['unique_titles_count']}")
    print(f"duplicate_titles_count: {report['duplicate_titles_count']}")
    print(f"output_file: {report['output_file']}")


def main() -> int:
    index_payload = _load_json(INDEX_PATH)
    package_id = _resolve_latest_package(index_payload)

    package_dir = PUBLISH_PACKAGES_DIR / package_id
    feed_path = package_dir / FINAL_FEED_NAME
    output_file = package_dir / AUDIT_FILE_NAME

    rows = _read_feed_rows(feed_path)
    report = _build_report(package_id, rows, output_file)

    _write_audit(output_file, report)
    _print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
