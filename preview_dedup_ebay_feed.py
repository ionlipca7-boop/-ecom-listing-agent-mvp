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


def _load_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            return [dict(row) for row in reader]
    except OSError as exc:
        raise ValueError(f"failed_to_read_csv: {csv_path.as_posix()}") from exc


def _dedup_by_title(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    seen_titles: set[str] = set()
    deduped_rows: list[dict[str, str]] = []
    removed_titles: list[str] = []

    for row in rows:
        title = (row.get("title") or "").strip()
        if title in seen_titles:
            if title not in removed_titles:
                removed_titles.append(title)
            continue
        seen_titles.add(title)
        deduped_rows.append(row)

    return deduped_rows, removed_titles


def main() -> int:
    index_payload = _load_json(INDEX_PATH)
    package_id = _resolve_latest_package(index_payload)

    csv_path = PUBLISH_PACKAGES_DIR / package_id / "ebay_feed.csv"
    rows = _load_csv_rows(csv_path)

    deduped_rows, removed_duplicate_titles = _dedup_by_title(rows)

    total_items_before = len(rows)
    total_items_after = len(deduped_rows)
    removed_duplicates_count = total_items_before - total_items_after
    kept_titles_sample = [((row.get("title") or "").strip()) for row in deduped_rows[:5]]

    print(f"package_id: {package_id}")
    print(f"total_items_before: {total_items_before}")
    print(f"total_items_after: {total_items_after}")
    print(f"removed_duplicates_count: {removed_duplicates_count}")
    print("removed_duplicate_titles:", json.dumps(removed_duplicate_titles, ensure_ascii=False))
    print("kept_titles_sample:", json.dumps(kept_titles_sample, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
