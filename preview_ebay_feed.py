import csv
import json
from collections import Counter
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


def _print_first_5_rows(rows: list[dict[str, str]]) -> None:
    print("first_5_rows:")
    print("title | price | category")
    for row in rows[:5]:
        title = (row.get("title") or "").strip()
        price = (row.get("price") or "").strip()
        category = (row.get("category") or "").strip()
        print(f"{title} | {price} | {category}")


def _print_category_summary(rows: list[dict[str, str]]) -> None:
    print("category_summary:")
    counts = Counter((row.get("category") or "").strip() for row in rows)

    if not counts:
        return

    for category_name, count in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"{category_name} = {count}")


def main() -> int:
    index_payload = _load_json(INDEX_PATH)
    package_id = _resolve_latest_package(index_payload)

    csv_path = PUBLISH_PACKAGES_DIR / package_id / "ebay_feed.csv"
    rows = _load_csv_rows(csv_path)

    print(f"package_id: {package_id}")
    print(f"total_items: {len(rows)}")
    _print_first_5_rows(rows)
    _print_category_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
