import json
from datetime import datetime, timezone
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"


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


def _write_summary(summary_file: Path, payload: dict) -> None:
    try:
        summary_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to write summary file: {summary_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    input_file = package_dir / "ebay_upload_ready_v2.csv"
    validation_file = package_dir / "ebay_upload_ready_v2_validation.json"
    summary_file = package_dir / "ebay_upload_ready_v2_summary.json"

    validation_payload = _load_json_file(validation_file, "validation file")
    summary_payload = validation_payload.get("summary")

    if not isinstance(summary_payload, dict):
        raise RuntimeError("validation summary is missing or invalid")

    checks_payload = validation_payload.get("checks")
    valid = summary_payload.get("valid")
    if not isinstance(valid, bool):
        if isinstance(checks_payload, dict):
            valid = all(bool(value) for value in checks_payload.values())
        else:
            raise RuntimeError("validation valid flag is missing or invalid")

    total_rows = summary_payload.get("total_rows")
    if not isinstance(total_rows, int):
        raise RuntimeError("validation total_rows is missing or invalid")

    total_columns = summary_payload.get("header_columns")
    if not isinstance(total_columns, int):
        raise RuntimeError("validation header_columns is missing or invalid")

    template_file = validation_payload.get("template_file")
    if not isinstance(template_file, str) or not template_file:
        raise RuntimeError("validation template_file is missing or invalid")

    summary = {
        "package_id": package_id,
        "input_file": input_file.as_posix(),
        "validation_file": validation_file.as_posix(),
        "total_rows": total_rows,
        "total_columns": total_columns,
        "valid": valid,
        "template_file": template_file,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    _write_summary(summary_file, summary)

    print(f"package_id: {package_id}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"validation_file: {validation_file.as_posix()}")
    print(f"summary_file: {summary_file.as_posix()}")
    print(f"valid: {valid}")
    print(f"total_rows: {total_rows}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
