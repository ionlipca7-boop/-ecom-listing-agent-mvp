import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"

CSV_COLUMNS = [
    "title",
    "description",
    "price",
    "category",
    "condition",
    "quantity",
    "format",
    "duration",
    "shipping_profile",
    "return_profile",
    "payment_profile",
]

DEFAULTS = {
    "condition": "New",
    "quantity": 1,
    "format": "FixedPrice",
    "duration": "GTC",
    "shipping_profile": "",
    "return_profile": "",
    "payment_profile": "",
}


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


def _build_csv_rows(manifest_payload: dict) -> list[dict]:
    items = manifest_payload.get("items", [])
    if not isinstance(items, list):
        return []

    rows: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue

        row = {
            "title": item.get("title", "") or "",
            "description": item.get("description", "") or "",
            "price": item.get("price", "") or "",
            "category": item.get("category", "") or "",
            **DEFAULTS,
        }
        rows.append(row)
    return rows


def main() -> int:
    index_payload = _load_json(INDEX_PATH)
    package_id = _resolve_latest_package(index_payload)

    package_dir = PUBLISH_PACKAGES_DIR / package_id
    manifest_path = package_dir / "manifest.json"
    output_path = package_dir / "ebay_feed.csv"

    manifest_payload = _load_json(manifest_path)
    csv_rows = _build_csv_rows(manifest_payload)

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"package_id: {package_id}")
    print(f"total_items: {len(csv_rows)}")
    print(f"output_file: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
