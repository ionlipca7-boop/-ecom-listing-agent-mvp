import csv
import json
import sys
from pathlib import Path


PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
UPLOAD_FILENAME = "ebay_upload_ready_v2.csv"
VALIDATION_FILENAME = "ebay_upload_ready_v2_validation.json"
REPORT_FILENAME = "compare_ebay_template_vs_upload_v2.json"
MIN_TEMPLATE_HEADER_COLUMNS = 20


def _load_json_file(file_path: Path, context: str) -> dict:
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read {context}: {file_path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError(f"{context} must be a JSON object: {file_path.as_posix()}")

    return payload


def _load_latest_package_id(index_path: Path) -> str:
    if not index_path.exists() or not index_path.is_file():
        raise RuntimeError(f"publish index not found: {index_path.as_posix()}")

    payload = _load_json_file(index_path, "publish index")
    latest_package = payload.get("latest_package")

    if not isinstance(latest_package, str) or not latest_package.strip():
        raise RuntimeError("latest_package is missing in publish index")

    return latest_package.strip()


def _resolve_template_file(validation_payload: dict, validation_file: Path) -> Path:
    template_file = validation_payload.get("template_file")

    if not isinstance(template_file, str) or not template_file.strip():
        raise RuntimeError(
            f"validation template_file is missing or invalid: {validation_file.as_posix()}"
        )

    raw_template_path = Path(template_file.strip())
    candidate_paths: list[Path] = []

    if raw_template_path.is_absolute():
        candidate_paths.append(raw_template_path)
    else:
        candidate_paths.append(Path.cwd() / raw_template_path)
        candidate_paths.append(validation_file.parent / raw_template_path)

        if raw_template_path.parts and raw_template_path.parts[0] == "templates":
            candidate_paths.append(Path.cwd() / raw_template_path.name)

        candidate_paths.append(Path.cwd() / "templates" / raw_template_path.name)

    seen = set()
    normalized_candidates: list[Path] = []
    for path in candidate_paths:
        normalized = path.resolve()
        key = normalized.as_posix()
        if key not in seen:
            seen.add(key)
            normalized_candidates.append(normalized)

    for candidate in normalized_candidates:
        if candidate.exists() and candidate.is_file():
            return candidate

    checked_paths = ", ".join(path.as_posix() for path in normalized_candidates)
    raise RuntimeError(f"template file not found; checked: {checked_paths}")


def _read_upload_header(csv_file: Path, context: str) -> list[str]:
    try:
        with csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
    except OSError as exc:
        raise RuntimeError(f"failed to read {context}: {csv_file.as_posix()}") from exc

    if not isinstance(header, list) or not header:
        raise RuntimeError(f"missing CSV header in {context}: {csv_file.as_posix()}")

    cleaned = [str(cell).strip() for cell in header]
    if not any(cleaned):
        raise RuntimeError(f"empty CSV header in {context}: {csv_file.as_posix()}")

    return cleaned


def _read_template_header(csv_file: Path, context: str) -> list[str]:
    try:
        with csv_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=";")
            rows = list(reader)
    except OSError as exc:
        raise RuntimeError(f"failed to read {context}: {csv_file.as_posix()}") from exc

    if not rows:
        raise RuntimeError(f"template file is empty: {csv_file.as_posix()}")

    best_row: list[str] | None = None
    best_non_empty_count = 0

    for row in rows:
        cleaned = [str(cell).strip() for cell in row]
        non_empty = [cell for cell in cleaned if cell]
        non_empty_count = len(non_empty)

        if non_empty_count == 0:
            continue

        if non_empty_count > best_non_empty_count:
            best_non_empty_count = non_empty_count
            best_row = cleaned

        if non_empty_count >= MIN_TEMPLATE_HEADER_COLUMNS:
            return cleaned

    if best_row is not None:
        raise RuntimeError(
            "template header row not found; "
            f"best row has only {best_non_empty_count} columns, expected at least "
            f"{MIN_TEMPLATE_HEADER_COLUMNS}: {csv_file.as_posix()}"
        )

    raise RuntimeError(f"template header row not found: {csv_file.as_posix()}")


def _compare_headers(upload_header: list[str], template_header: list[str]) -> dict:
    upload_set = set(upload_header)
    template_set = set(template_header)

    upload_only_columns = [column for column in upload_header if column not in template_set]
    template_only_columns = [column for column in template_header if column not in upload_set]
    common_columns = [column for column in upload_header if column in template_set]

    first_mismatch_index = None
    first_mismatch_upload_column = None
    first_mismatch_template_column = None

    max_len = max(len(upload_header), len(template_header))
    for index in range(max_len):
        upload_value = upload_header[index] if index < len(upload_header) else None
        template_value = template_header[index] if index < len(template_header) else None
        if upload_value != template_value:
            first_mismatch_index = index
            first_mismatch_upload_column = upload_value
            first_mismatch_template_column = template_value
            break

    exact_order_match = upload_header == template_header
    upload_subset_of_template = upload_set.issubset(template_set)

    summary_parts = []
    if upload_subset_of_template:
        summary_parts.append("upload header is a subset of template header")
    else:
        summary_parts.append("upload header is not a subset of template header")

    if exact_order_match:
        summary_parts.append("column order matches exactly")
    else:
        summary_parts.append("column order does not match")

    if first_mismatch_index is None:
        summary_parts.append("no index mismatch detected")
    else:
        summary_parts.append(f"first mismatch at index {first_mismatch_index} (0-based)")

    return {
        "upload_columns_count": len(upload_header),
        "template_columns_count": len(template_header),
        "upload_only_columns": upload_only_columns,
        "template_only_columns": template_only_columns,
        "common_columns": common_columns,
        "first_mismatch_index": first_mismatch_index,
        "first_mismatch_upload_column": first_mismatch_upload_column,
        "first_mismatch_template_column": first_mismatch_template_column,
        "exact_order_match": exact_order_match,
        "exact_order_mismatch_summary": "; ".join(summary_parts),
    }


def _write_report(report_file: Path, payload: dict) -> None:
    try:
        report_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError as exc:
        raise RuntimeError(f"failed to write report file: {report_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    if not package_dir.exists() or not package_dir.is_dir():
        raise RuntimeError(f"package directory not found: {package_dir.as_posix()}")

    upload_file = package_dir / UPLOAD_FILENAME
    validation_file = package_dir / VALIDATION_FILENAME
    report_file = package_dir / REPORT_FILENAME

    if not upload_file.exists() or not upload_file.is_file():
        raise RuntimeError(f"upload file not found: {upload_file.as_posix()}")

    if not validation_file.exists() or not validation_file.is_file():
        raise RuntimeError(f"validation file not found: {validation_file.as_posix()}")

    validation_payload = _load_json_file(validation_file, "validation report")
    template_file = _resolve_template_file(validation_payload, validation_file)

    upload_header = _read_upload_header(upload_file, "upload CSV")
    template_header = _read_template_header(template_file, "template CSV")

    compare_payload = _compare_headers(upload_header, template_header)
    report_payload = {
        "package_id": package_id,
        **compare_payload,
    }

    _write_report(report_file, report_payload)

    print(f"package_id: {package_id}")
    print(f"upload_columns_count: {report_payload['upload_columns_count']}")
    print(f"template_columns_count: {report_payload['template_columns_count']}")
    print(f"template_only_columns_count: {len(report_payload['template_only_columns'])}")
    print(f"upload_only_columns_count: {len(report_payload['upload_only_columns'])}")
    print(f"report_file: {report_file.as_posix()}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)