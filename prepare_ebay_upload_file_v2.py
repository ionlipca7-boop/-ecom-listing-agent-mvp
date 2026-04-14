import csv
import json
from pathlib import Path
from typing import Iterable

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
TEMPLATE_PATH = Path("templates") / "ebay_category_template.csv"


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


def _read_final_csv(input_file: Path) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as src:
            reader = csv.DictReader(src)
            fieldnames = reader.fieldnames
            if not fieldnames:
                raise RuntimeError("final CSV has no header")
            rows = list(reader)
    except OSError as exc:
        raise RuntimeError(f"failed to read final CSV: {input_file.as_posix()}") from exc

    return fieldnames, rows


def _normalize_row(values: Iterable[str]) -> list[str]:
    return [value.strip() for value in values]


def _is_meta_or_info_row(row: list[str]) -> bool:
    non_empty = [cell for cell in row if cell]
    if not non_empty:
        return True

    first = non_empty[0].lower()
    return (
        first.startswith("#")
        or first.startswith("sep=")
        or first.startswith("meta")
        or first.startswith("info")
        or first.startswith("template")
    )


def _find_template_header(template_path: Path, final_header: list[str]) -> list[str]:
    try:
        with template_path.open("r", encoding="utf-8-sig", newline="") as src:
            reader = csv.reader(src)
            template_rows = [_normalize_row(row) for row in reader]
    except OSError as exc:
        raise RuntimeError(f"failed to read template CSV: {template_path.as_posix()}") from exc

    if not template_rows:
        raise RuntimeError("template CSV is empty")

    final_columns = {col.strip() for col in final_header if col.strip()}
    best_match: list[str] | None = None
    best_score = -1

    for row in template_rows:
        row_columns = [cell for cell in row if cell]
        if not row_columns or _is_meta_or_info_row(row):
            continue

        overlap = sum(1 for col in row_columns if col in final_columns)
        if overlap > best_score:
            best_score = overlap
            best_match = row_columns

        if final_columns and final_columns.issubset(set(row_columns)):
            return row_columns

    if best_match and best_score > 0:
        return best_match

    raise RuntimeError("failed to detect header row in template CSV")


def _write_upload_file(output_file: Path, template_header: list[str], rows: list[dict[str, str]]) -> int:
    try:
        with output_file.open("w", encoding="utf-8-sig", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=template_header, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                normalized = {column: row.get(column, "") for column in template_header}
                writer.writerow(normalized)
    except OSError as exc:
        raise RuntimeError(f"failed to write output CSV: {output_file.as_posix()}") from exc

    return len(rows)


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    input_file = package_dir / "ebay_feed_final.csv"
    output_file = package_dir / "ebay_upload_ready_v2.csv"

    final_header, rows = _read_final_csv(input_file)
    template_header = _find_template_header(TEMPLATE_PATH, final_header)
    total_items = _write_upload_file(output_file, template_header, rows)

    print(f"package_id: {package_id}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"template_file: {TEMPLATE_PATH.as_posix()}")
    print(f"output_file: {output_file.as_posix()}")
    print(f"total_items: {total_items}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
