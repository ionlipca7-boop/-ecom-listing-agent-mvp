import csv
import json
from datetime import datetime, timezone
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
UPLOAD_FILE_NAME = "ebay_upload_ready_v2.csv"
VALIDATION_FILE_NAME = "ebay_upload_ready_v2_validation.json"
INSPECTION_FILE_NAME = "export_bundle_v2_inspection.json"
AUDIT_FILE_NAME = "ebay_upload_contract_audit_v2.json"


class AuditError(RuntimeError):
    pass


def _load_json_file(file_path: Path, context: str) -> dict:
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AuditError(f"failed to read {context}: {file_path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise AuditError(f"{context} must be a JSON object")

    return payload


def _load_latest_package_id(index_path: Path) -> str:
    payload = _load_json_file(index_path, "publish index")
    latest_package = payload.get("latest_package")

    if not isinstance(latest_package, str) or not latest_package:
        raise AuditError("latest_package is missing in publish index")

    return latest_package


def _read_csv_header(file_path: Path, context: str) -> list[str]:
    try:
        with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
    except OSError as exc:
        raise AuditError(f"failed to read {context}: {file_path.as_posix()}") from exc

    if not header:
        raise AuditError(f"missing CSV header in {context}: {file_path.as_posix()}")

    return [column.strip() for column in header]


def _resolve_template_file(validation_payload: dict, package_dir: Path) -> Path:
    for key in ("template_file", "template_csv", "template_path", "template"):
        candidate = validation_payload.get(key)
        if isinstance(candidate, str) and candidate.strip():
            candidate_path = Path(candidate.strip())
            if candidate_path.is_absolute():
                return candidate_path
            package_candidate = (package_dir / candidate_path).resolve()
            if package_candidate.exists():
                return package_candidate
            return (Path.cwd() / candidate_path).resolve()

    raise AuditError("template file path is missing in validation payload")


def _header_diff(upload_header: list[str], template_header: list[str]) -> dict:
    header_order_matches_template = upload_header == template_header

    missing_columns = [column for column in template_header if column not in upload_header]
    extra_columns = [column for column in upload_header if column not in template_header]

    mismatch_index = None
    mismatch_upload = None
    mismatch_template = None

    max_len = max(len(upload_header), len(template_header))
    for index in range(max_len):
        upload_column = upload_header[index] if index < len(upload_header) else None
        template_column = template_header[index] if index < len(template_header) else None
        if upload_column != template_column:
            mismatch_index = index
            mismatch_upload = upload_column
            mismatch_template = template_column
            break

    return {
        "header_order_matches_template": header_order_matches_template,
        "missing_columns_count": len(missing_columns),
        "extra_columns_count": len(extra_columns),
        "first_mismatch_index": mismatch_index,
        "first_mismatch_upload_column": mismatch_upload,
        "first_mismatch_template_column": mismatch_template,
    }


def _conclusion(validation_valid: bool, inspection_valid: bool, header_matches: bool) -> tuple[str, str]:
    if validation_valid and inspection_valid and header_matches:
        return "ebay_upload_ready", "ready_for_merge"

    if inspection_valid and not header_matches:
        return "internal_export_only", "mapping_layer_needed"

    return "not_ebay_upload_ready", "prepare_fix_needed"


def _write_audit_file(path: Path, payload: dict) -> None:
    try:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise AuditError(f"failed to write audit file: {path.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    upload_file = package_dir / UPLOAD_FILE_NAME
    validation_file = package_dir / VALIDATION_FILE_NAME
    inspection_file = package_dir / INSPECTION_FILE_NAME

    validation_payload = _load_json_file(validation_file, "validation report")
    inspection_payload = _load_json_file(inspection_file, "inspection report")

    template_file = _resolve_template_file(validation_payload, package_dir)
    if not template_file.exists() or not template_file.is_file():
        raise AuditError(f"template file missing: {template_file.as_posix()}")

    upload_header = _read_csv_header(upload_file, "upload CSV")
    template_header = _read_csv_header(template_file, "template CSV")

    header_diff = _header_diff(upload_header, template_header)

    validation_valid = validation_payload.get("valid") is True
    inspection_valid = inspection_payload.get("valid") is True

    conclusion, recommended_next_layer = _conclusion(
        validation_valid=validation_valid,
        inspection_valid=inspection_valid,
        header_matches=header_diff["header_order_matches_template"],
    )

    audit_file = package_dir / AUDIT_FILE_NAME
    audit_payload = {
        "package_id": package_id,
        "upload_file": upload_file.as_posix(),
        "template_file": template_file.as_posix(),
        "inspection_file": inspection_file.as_posix(),
        "upload_columns_count": len(upload_header),
        "template_columns_count": len(template_header),
        "header_order_matches_template": header_diff["header_order_matches_template"],
        "validation_valid": validation_valid,
        "inspection_valid": inspection_valid,
        "missing_columns_count": header_diff["missing_columns_count"],
        "extra_columns_count": header_diff["extra_columns_count"],
        "first_mismatch_index": header_diff["first_mismatch_index"],
        "first_mismatch_upload_column": header_diff["first_mismatch_upload_column"],
        "first_mismatch_template_column": header_diff["first_mismatch_template_column"],
        "conclusion": conclusion,
        "recommended_next_layer": recommended_next_layer,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    _write_audit_file(audit_file, audit_payload)

    print(f"package_id: {package_id}")
    print(f"upload_columns: {len(upload_header)}")
    print(f"template_columns: {len(template_header)}")
    print(f"validation_valid: {validation_valid}")
    print(f"inspection_valid: {inspection_valid}")
    print(f"conclusion: {conclusion}")
    print(f"audit_file: {audit_file.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
