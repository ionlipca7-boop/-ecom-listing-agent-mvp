import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
TEMPLATES_DIR = Path("templates")
DEFAULT_TEMPLATE_FILE = TEMPLATES_DIR / "ebay_category_template.csv"


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


def _resolve_template_file() -> Path:
    if DEFAULT_TEMPLATE_FILE.is_file():
        return DEFAULT_TEMPLATE_FILE

    if not TEMPLATES_DIR.exists():
        raise RuntimeError(f"templates directory not found: {TEMPLATES_DIR.as_posix()}")

    if not TEMPLATES_DIR.is_dir():
        raise RuntimeError(f"templates path is not a directory: {TEMPLATES_DIR.as_posix()}")

    csv_candidates = [path for path in TEMPLATES_DIR.glob("*.csv") if path.is_file()]
    if not csv_candidates:
        raise RuntimeError(
            f"no template CSV found in {TEMPLATES_DIR.as_posix()} (expected {DEFAULT_TEMPLATE_FILE.as_posix()} or any *.csv)"
        )

    if len(csv_candidates) == 1:
        return csv_candidates[0]

    return max(csv_candidates, key=lambda path: path.stat().st_mtime)


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

    template_file = _resolve_template_file()

    input_file = package_dir / "ebay_feed_final.csv"
    output_file = package_dir / "ebay_upload_ready.csv"

    total_items = _copy_csv_preserve_schema(input_file, output_file)

    print(f"package_id: {package_id}")
    print(f"template_file: {template_file.as_posix()}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"output_file: {output_file.as_posix()}")
    print(f"total_items: {total_items}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
