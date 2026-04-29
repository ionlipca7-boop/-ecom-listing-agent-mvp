import csv
import json
from datetime import datetime, timezone
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
TEMPLATES_DIR = Path("templates")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
REPORT_FILE_NAME = "compare_ebay_template_vs_upload_v2.json"
TEMPLATE_DELIMITER_CANDIDATES = (",", "\t", ";", "|")


def _load_json_file(file_path: Path, context: str) -> dict:
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read {context}: {file_path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError(f"{context} must be a JSON object")

    return payload


def _load_latest_package_id(index_path: Path) -> str:
    payload = _load_json_file(index_path, "index file")
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


def _score_template_row(cells: list[str], delimiter: str) -> tuple[int, int, int, int]:
    non_empty_cells = [cell for cell in cells if cell.strip()]
    width = len(cells)
    non_empty_width = len(non_empty_cells)
    unique_non_empty_width = len(set(non_empty_cells))
    preferred_delimiter = 1 if delimiter == "," else 0
    return (width, non_empty_width, unique_non_empty_width, preferred_delimiter)


def _detect_template_header(csv_file: Path) -> list[str]:
    try:
        lines = csv_file.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        raise RuntimeError(f"failed to read CSV file: {csv_file.as_posix()}") from exc

    best_header: list[str] = []
    best_score = (-1, -1, -1, -1)

    for line in lines:
        if not line.strip():
            continue

        for delimiter in TEMPLATE_DELIMITER_CANDIDATES:
            cells = next(csv.reader([line], delimiter=delimiter))
            cleaned_cells = [str(cell).strip() for cell in cells]
            score = _score_template_row(cleaned_cells, delimiter)
            if score > best_score:
                best_header = cleaned_cells
                best_score = score

    return best_header


def _read_csv_header(csv_file: Path) -> list[str]:
    try:
        with csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            return [str(cell).strip() for cell in (next(reader, None) or [])]
    except OSError as exc:
        raise RuntimeError(f"failed to read CSV file: {csv_file.as_posix()}") from exc


def _collect_order_mismatches(template_header: list[str], upload_header: list[str]) -> list[dict]:
    upload_positions = {column_name: index for index, column_name in enumerate(upload_header)}
    mismatches: list[dict] = []

    for template_index, column_name in enumerate(template_header):
        upload_index = upload_positions.get(column_name)
        if upload_index is not None and upload_index != template_index:
            mismatches.append(
                {
                    "column": column_name,
                    "template_index": template_index,
                    "upload_index": upload_index,
                }
            )

    return mismatches


def _write_report(report_file: Path, payload: dict) -> None:
    try:
        report_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to write report file: {report_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    template_file = _resolve_template_file(TEMPLATES_DIR)
    upload_file = package_dir / "ebay_upload_ready_v2.csv"
    report_file = package_dir / REPORT_FILE_NAME

    file_exists = upload_file.exists() and upload_file.is_file()
    template_header = _detect_template_header(template_file)
    upload_header = _read_csv_header(upload_file) if file_exists else []

    template_only_columns = [column for column in template_header if column not in set(upload_header)]
    upload_only_columns = [column for column in upload_header if column not in set(template_header)]
    order_mismatches = _collect_order_mismatches(template_header, upload_header)

    exact_header_match = file_exists and template_header == upload_header

    report_payload = {
        "package_id": package_id,
        "template_file": template_file.as_posix(),
        "upload_file": upload_file.as_posix(),
        "report_file": report_file.as_posix(),
        "file_exists": file_exists,
        "summary": {
            "template_columns": len(template_header),
            "upload_columns": len(upload_header),
            "template_only_columns": template_only_columns,
            "upload_only_columns": upload_only_columns,
            "order_mismatches": order_mismatches,
            "exact_header_match": exact_header_match,
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    _write_report(report_file, report_payload)

    print(f"package_id: {package_id}")
    print(f"upload_file: {upload_file.as_posix()}")
    print(f"template_file: {template_file.as_posix()}")
    print(f"exact_header_match: {exact_header_match}")
    print(f"report_file: {report_file.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
