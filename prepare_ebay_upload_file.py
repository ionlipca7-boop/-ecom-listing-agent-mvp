import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"


def _load_latest_package_id(index_path: Path) -> str:
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read index file: {index_path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("publish index must be a JSON object")

    latest_package = payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        raise RuntimeError("latest_package is missing in publish index")

    return latest_package


def _copy_csv_preserve_schema(input_file: Path, output_file: Path) -> int:
    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as src:
            reader = csv.DictReader(src)
            fieldnames = reader.fieldnames
            if not fieldnames:
                raise RuntimeError("input CSV has no header")

            rows = list(reader)
    except OSError as exc:
        raise RuntimeError(f"failed to read input CSV: {input_file.as_posix()}") from exc

    try:
        with output_file.open("w", encoding="utf-8-sig", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        raise RuntimeError(f"failed to write output CSV: {output_file.as_posix()}") from exc

    return len(rows)


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    input_file = package_dir / "ebay_feed_final.csv"
    output_file = package_dir / "ebay_upload_ready.csv"

    total_items = _copy_csv_preserve_schema(input_file, output_file)

    print(f"package_id: {package_id}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"output_file: {output_file.as_posix()}")
    print(f"total_items: {total_items}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
