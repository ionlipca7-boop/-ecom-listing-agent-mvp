import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
DEDUP_FILE = "ebay_feed_dedup.csv"
DEFAULT_FILE = "ebay_feed.csv"
OUTPUT_FILE = "ebay_feed_final.csv"


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


def _select_input_file(package_dir: Path) -> Path:
    dedup_path = package_dir / DEDUP_FILE
    if dedup_path.exists():
        return dedup_path

    fallback_path = package_dir / DEFAULT_FILE
    if fallback_path.exists():
        return fallback_path

    raise ValueError("ebay_feed_source_not_found")


def _copy_csv(input_path: Path, output_path: Path) -> int:
    with input_path.open("r", encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError("csv_header_not_found")

        rows = list(reader)

    with output_path.open("w", encoding="utf-8-sig", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main() -> int:
    index_payload = _load_json(INDEX_PATH)
    package_id = _resolve_latest_package(index_payload)

    package_dir = PUBLISH_PACKAGES_DIR / package_id
    input_path = _select_input_file(package_dir)
    output_path = package_dir / OUTPUT_FILE

    total_items = _copy_csv(input_path, output_path)

    print(f"package_id: {package_id}")
    print(f"input_file_used: {input_path.as_posix()}")
    print(f"total_items: {total_items}")
    print(f"output_file: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
