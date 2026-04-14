import json
from datetime import datetime, timezone
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
BUNDLE_DIR_NAME = "export_bundle_v2"
ZIP_FILE_NAME = "export_bundle_v2.zip"
ZIP_MANIFEST_FILE_NAME = "export_bundle_v2_zip_manifest.json"
INSPECTION_FILE_NAME = "export_bundle_v2_inspection.json"
EXPECTED_BUNDLE_FILES = (
    "ebay_upload_ready_v2.csv",
    "ebay_upload_ready_v2_validation.json",
    "ebay_upload_ready_v2_summary.json",
    "export_bundle_v2_manifest.json",
)


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


def _verify_bundle_files(bundle_dir: Path) -> tuple[bool, list[str], int]:
    missing_files: list[str] = []

    for file_name in EXPECTED_BUNDLE_FILES:
        expected_path = bundle_dir / file_name
        if not expected_path.exists() or not expected_path.is_file():
            missing_files.append(file_name)

    return len(missing_files) == 0, missing_files, len(EXPECTED_BUNDLE_FILES)


def _verify_manifest_entries(manifest_payload: dict) -> tuple[bool, list[str]]:
    included_files = manifest_payload.get("included_files")

    if not isinstance(included_files, list):
        return False, ["included_files"]

    included_file_names = {item for item in included_files if isinstance(item, str)}
    missing_entries = [
        file_name for file_name in EXPECTED_BUNDLE_FILES if file_name not in included_file_names
    ]

    return len(missing_entries) == 0, missing_entries


def _write_inspection_file(inspection_file: Path, payload: dict) -> None:
    try:
        inspection_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to write inspection file: {inspection_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id
    bundle_dir = package_dir / BUNDLE_DIR_NAME
    zip_file = package_dir / ZIP_FILE_NAME
    zip_manifest_file = package_dir / ZIP_MANIFEST_FILE_NAME
    inspection_file = package_dir / INSPECTION_FILE_NAME

    bundle_exists = bundle_dir.exists() and bundle_dir.is_dir()
    zip_exists = zip_file.exists() and zip_file.is_file()

    if not bundle_exists:
        raise RuntimeError(f"bundle directory missing: {bundle_dir.as_posix()}")
    if not zip_exists:
        raise RuntimeError(f"zip file missing: {zip_file.as_posix()}")

    bundle_files_ok, missing_bundle_files, files_checked = _verify_bundle_files(bundle_dir)

    zip_manifest_payload = _load_json_file(zip_manifest_file, "zip manifest file")
    manifest_files_ok, missing_manifest_entries = _verify_manifest_entries(zip_manifest_payload)

    manifest_valid = zip_manifest_payload.get("valid") is True
    valid = bundle_exists and zip_exists and bundle_files_ok and manifest_files_ok and manifest_valid

    inspection_payload = {
        "package_id": package_id,
        "bundle_dir": bundle_dir.as_posix(),
        "zip_file": zip_file.as_posix(),
        "zip_manifest_file": zip_manifest_file.as_posix(),
        "inspection_file": inspection_file.as_posix(),
        "bundle_exists": bundle_exists,
        "zip_exists": zip_exists,
        "expected_files": list(EXPECTED_BUNDLE_FILES),
        "missing_bundle_files": missing_bundle_files,
        "missing_manifest_entries": missing_manifest_entries,
        "manifest_valid": manifest_valid,
        "files_checked": files_checked,
        "valid": valid,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    _write_inspection_file(inspection_file, inspection_payload)

    print(f"package_id: {package_id}")
    print(f"bundle_dir: {bundle_dir.as_posix()}")
    print(f"zip_file: {zip_file.as_posix()}")
    print(f"inspection_file: {inspection_file.as_posix()}")
    print(f"valid: {valid}")
    print(f"files_checked: {files_checked}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
