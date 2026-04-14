import csv
import json
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
REQUIRED_FIELDS = ("title", "description", "price", "category")


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


def _normalized_text(value: str | None) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()


def _duplicate_titles(rows: list[dict]) -> tuple[int, list[str]]:
    title_counter: Counter[str] = Counter()
    for row in rows:
        normalized_title = _normalized_text(row.get("title"))
        if normalized_title:
            title_counter[normalized_title] += 1

    duplicates = sorted([title for title, count in title_counter.items() if count > 1])
    return len(duplicates), duplicates


def _missing_required_fields(rows: list[dict]) -> tuple[int, list[dict]]:
    missing_rows: list[dict] = []

    for index, row in enumerate(rows, start=1):
        missing_fields = [field for field in REQUIRED_FIELDS if not _normalized_text(row.get(field))]
        if missing_fields:
            missing_rows.append({"row": index, "fields": missing_fields})

    return len(missing_rows), missing_rows


def _category_summary(rows: list[dict]) -> dict[str, int]:
    categories: Counter[str] = Counter()
    for row in rows:
        category = _normalized_text(row.get("category")) or "<missing>"
        categories[category] += 1
    return dict(sorted(categories.items(), key=lambda item: item[0]))


def _price_summary(rows: list[dict]) -> dict:
    prices: list[Decimal] = []

    for row in rows:
        raw_price = _normalized_text(row.get("price"))
        if not raw_price:
            continue
        try:
            prices.append(Decimal(raw_price))
        except InvalidOperation:
            continue

    if not prices:
        return {
            "min_price": None,
            "max_price": None,
            "unique_prices": 0,
        }

    return {
        "min_price": str(min(prices)),
        "max_price": str(max(prices)),
        "unique_prices": len(set(prices)),
    }


def _print_audit(report: dict) -> None:
    print(f"package_id: {report['package_id']}")
    print(f"total_items: {report['total_items']}")
    print(f"duplicate_titles_count: {report['duplicate_titles_count']}")
    print(f"duplicate_titles_list: {json.dumps(report['duplicate_titles_list'], ensure_ascii=False)}")
    print(f"missing_required_fields_count: {report['missing_required_fields_count']}")
    print(
        "missing_required_fields_rows: "
        f"{json.dumps(report['missing_required_fields_rows'], ensure_ascii=False)}"
    )
    print(f"category_summary: {json.dumps(report['category_summary'], ensure_ascii=False)}")
    print(f"price_summary: {json.dumps(report['price_summary'], ensure_ascii=False)}")


def main() -> int:
    index_payload = _load_json(INDEX_PATH)
    package_id = _resolve_latest_package(index_payload)

    feed_path = PUBLISH_PACKAGES_DIR / package_id / "ebay_feed.csv"
    rows = _read_feed_rows(feed_path)

    duplicate_titles_count, duplicate_titles_list = _duplicate_titles(rows)
    missing_required_fields_count, missing_required_fields_rows = _missing_required_fields(rows)

    report = {
        "package_id": package_id,
        "total_items": len(rows),
        "duplicate_titles_count": duplicate_titles_count,
        "duplicate_titles_list": duplicate_titles_list,
        "missing_required_fields_count": missing_required_fields_count,
        "missing_required_fields_rows": missing_required_fields_rows,
        "category_summary": _category_summary(rows),
        "price_summary": _price_summary(rows),
    }

    _print_audit(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
