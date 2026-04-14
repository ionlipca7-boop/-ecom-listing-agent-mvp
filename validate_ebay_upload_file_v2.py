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
    strict_candidates = sorted(
        templates_dir.glob("eBay-category-listing-template*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if strict_candidates:
        return strict_candidates[0]

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
            header = next(reader, None)
    except OSError as exc:
        raise RuntimeError(f"failed to read CSV file: {csv_file.as_posix()}") from exc

    if header is None:
        return []

    return [str(cell) for cell in header]


def _duplicate_values(items: list[str]) -> list[str]:
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return sorted(duplicates)


def _validate_rows_shape(input_file: Path, expected_columns: int) -> tuple[int, list[int]]:
    total_rows = 0
    invalid_rows: list[int] = []

    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            for row_number, row in enumerate(reader, start=2):
                total_rows += 1
                if len(row) != expected_columns:
                    invalid_rows.append(row_number)
    except OSError as exc:
        raise RuntimeError(f"failed to read input CSV: {input_file.as_posix()}") from exc

    return total_rows, invalid_rows


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

    upload_header: list[str] = []
    template_header: list[str] = _read_header(template_file)
    total_rows = 0
    invalid_row_numbers: list[int] = []
    header_duplicates: list[str] = []

    if file_exists:
        upload_header = _read_header(input_file)

        if upload_header:
            header_duplicates = _duplicate_values(upload_header)
            total_rows, invalid_row_numbers = _validate_rows_shape(input_file, len(upload_header))

    header_non_empty = len(upload_header) > 0
    header_match = upload_header == template_header if file_exists else False
    has_data_rows = total_rows > 0
    has_no_duplicate_headers = len(header_duplicates) == 0
    rows_shape_ok = len(invalid_row_numbers) == 0

    valid = all(
        [
            file_exists,
            header_non_empty,
            header_match,
            has_data_rows,
            has_no_duplicate_headers,
            rows_shape_ok,
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
            "header_match": header_match,
            "has_data_rows": has_data_rows,
            "has_no_duplicate_headers": has_no_duplicate_headers,
            "rows_shape_ok": rows_shape_ok,
        },
        "summary": {
            "total_rows": total_rows,
            "header_columns": len(upload_header),
            "template_columns": len(template_header),
            "duplicate_headers": header_duplicates,
            "invalid_row_numbers": invalid_row_numbers,
            "valid": valid,
        },
    }

    _write_report(report_file, report)

    print(f"package_id: {package_id}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"template_file: {template_file.as_posix()}")
    print(f"total_rows: {total_rows}")
    print(f"header_match: {header_match}")
    print(f"valid: {valid}")
    print(f"report_file: {report_file.as_posix()}")

    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
