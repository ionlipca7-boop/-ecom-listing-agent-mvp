import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"


def _load_json(path: Path) -> dict:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"failed_to_read_json: {path.as_posix()}") from exc

    if not isinstance(raw, dict):
        raise ValueError(f"invalid_json_object: {path.as_posix()}")
    return raw


def _resolve_latest_package(index_payload: dict) -> str:
    latest_package = index_payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        raise ValueError("latest_package_not_found")
    return latest_package


def _normalize_title(title: str) -> str:
    return " ".join(title.casefold().split())


def _load_csv_rows(csv_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            rows = [dict(row) for row in reader]
    except OSError as exc:
        raise ValueError(f"failed_to_read_csv: {csv_path.as_posix()}") from exc

    if not fieldnames:
        raise ValueError(f"csv_header_not_found: {csv_path.as_posix()}")

    return rows, fieldnames


def _dedup_by_normalized_title(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen_titles: set[str] = set()
    deduped_rows: list[dict[str, str]] = []

    for row in rows:
        normalized_title = _normalize_title((row.get("title") or ""))
        if normalized_title in seen_titles:
            continue
        seen_titles.add(normalized_title)
        deduped_rows.append(row)

    return deduped_rows


def main() -> int:
    index_payload = _load_json(INDEX_PATH)
    package_id = _resolve_latest_package(index_payload)

    package_dir = PUBLISH_PACKAGES_DIR / package_id
    input_path = package_dir / "ebay_feed.csv"
    output_path = package_dir / "ebay_feed_dedup.csv"

    rows, fieldnames = _load_csv_rows(input_path)
    deduped_rows = _dedup_by_normalized_title(rows)

    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped_rows)

    total_items_before = len(rows)
    total_items_after = len(deduped_rows)

    print(f"package_id: {package_id}")
    print(f"total_items_before: {total_items_before}")
    print(f"total_items_after: {total_items_after}")
    print(f"removed_duplicates_count: {total_items_before - total_items_after}")
    print(f"output_file: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
