import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
TEMPLATES_DIR = Path("templates")
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


def _resolve_template_file(templates_dir: Path) -> Path:
    preferred_candidates = sorted(
        templates_dir.glob("eBay-category-listing-template*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if preferred_candidates:
        return preferred_candidates[0]

    fallback_candidates = sorted(
        templates_dir.glob("*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if fallback_candidates:
        return fallback_candidates[0]

    raise RuntimeError(f"no CSV template files found in: {templates_dir.as_posix()}")


def _read_header(csv_file: Path) -> list[str]:
    try:
        with csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            return [str(cell) for cell in (next(reader, None) or [])]
    except OSError as exc:
        raise RuntimeError(f"failed to read CSV file: {csv_file.as_posix()}") from exc


def _duplicate_values(items: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return sorted(duplicates)


def _validate_rows_shape(input_file: Path, expected_columns: int) -> tuple[int, list[int]]:
    total_rows = 0
    invalid_row_numbers: list[int] = []

    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            for row_number, row in enumerate(reader, start=2):
                total_rows += 1
                if len(row) != expected_columns:
                    invalid_row_numbers.append(row_number)
    except OSError as exc:
        raise RuntimeError(f"failed to read input CSV: {input_file.as_posix()}") from exc

    return total_rows, invalid_row_numbers


def _write_report(report_file: Path, payload: dict) -> None:
    try:
        report_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to write report file: {report_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    template_file = _resolve_template_file(TEMPLATES_DIR)
    input_file = package_dir / "ebay_upload_ready_v2.csv"
    report_file = package_dir / "ebay_upload_ready_v2_validation.json"

    file_exists = input_file.exists()
    template_header = _read_header(template_file)

    upload_header: list[str] = []
    total_rows = 0
    invalid_row_numbers: list[int] = []
    duplicate_headers: list[str] = []

    if file_exists:
        upload_header = _read_header(input_file)
        if upload_header:
            duplicate_headers = _duplicate_values(upload_header)
            total_rows, invalid_row_numbers = _validate_rows_shape(input_file, len(upload_header))

    header_non_empty = len(upload_header) > 0
    has_data_rows = total_rows > 0
    header_order_matches_template = upload_header == template_header if file_exists else False
    row_column_counts_match_header = len(invalid_row_numbers) == 0
    no_duplicate_header_names = len(duplicate_headers) == 0

    valid = all(
        [
            file_exists,
            header_non_empty,
            has_data_rows,
            header_order_matches_template,
            row_column_counts_match_header,
            no_duplicate_header_names,
        ]
    )

    report = {
        "package_id": package_id,
        "input_file": input_file.as_posix(),
        "template_file": template_file.as_posix(),
        "report_file": report_file.as_posix(),
        "checks": {
            "file_exists": file_exists,
            "header_non_empty": header_non_empty,
            "has_data_rows": has_data_rows,
            "header_order_matches_template": header_order_matches_template,
            "row_column_counts_match_header": row_column_counts_match_header,
            "no_duplicate_header_names": no_duplicate_header_names,
        },
        "summary": {
            "total_rows": total_rows,
            "header_columns": len(upload_header),
            "template_columns": len(template_header),
            "invalid_row_numbers": invalid_row_numbers,
            "duplicate_headers": duplicate_headers,
            "valid": valid,
        },
    }

    _write_report(report_file, report)

    print(f"package_id: {package_id}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"template_file: {template_file.as_posix()}")
    print(f"valid: {valid}")
    print(f"total_rows: {total_rows}")
    print(f"report_file: {report_file.as_posix()}")

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
