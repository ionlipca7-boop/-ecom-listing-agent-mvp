import json
from datetime import datetime, timezone
from pathlib import Path
import zipfile

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
BUNDLE_DIR_NAME = "export_bundle_v2"
ZIP_FILE_NAME = "export_bundle_v2.zip"
ZIP_MANIFEST_FILE_NAME = "export_bundle_v2_zip_manifest.json"


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


def _collect_bundle_files(bundle_dir: Path) -> list[Path]:
    files = sorted(path for path in bundle_dir.iterdir() if path.is_file())
    if not files:
        raise RuntimeError(f"bundle directory is empty: {bundle_dir.as_posix()}")
    return files


def _extract_bundle_stats(bundle_dir: Path) -> tuple[bool, int, int]:
    bundle_manifest_path = bundle_dir / "export_bundle_v2_manifest.json"
    bundle_manifest = _load_json_file(bundle_manifest_path, "bundle manifest file")

    valid = bundle_manifest.get("valid")
    total_rows = bundle_manifest.get("total_rows")
    total_columns = bundle_manifest.get("total_columns")

    if not isinstance(valid, bool):
        raise RuntimeError("bundle manifest valid is missing or invalid")
    if not isinstance(total_rows, int):
        raise RuntimeError("bundle manifest total_rows is missing or invalid")
    if not isinstance(total_columns, int):
        raise RuntimeError("bundle manifest total_columns is missing or invalid")

    return valid, total_rows, total_columns


def _create_zip_archive(bundle_dir: Path, zip_file: Path, files: list[Path]) -> list[str]:
    included_files: list[str] = []

    try:
        with zipfile.ZipFile(zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in files:
                archive_name = file_path.relative_to(bundle_dir).as_posix()
                archive.write(file_path, arcname=archive_name)
                included_files.append(archive_name)
    except OSError as exc:
        raise RuntimeError(f"failed to write zip archive: {zip_file.as_posix()}") from exc

    return included_files


def _write_manifest(manifest_file: Path, payload: dict) -> None:
    try:
        manifest_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to write manifest file: {manifest_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id
    bundle_dir = package_dir / BUNDLE_DIR_NAME

    if not bundle_dir.exists() or not bundle_dir.is_dir():
        raise RuntimeError(f"bundle directory missing: {bundle_dir.as_posix()}")

    bundle_files = _collect_bundle_files(bundle_dir)

    zip_file = package_dir / ZIP_FILE_NAME
    included_files = _create_zip_archive(bundle_dir, zip_file, bundle_files)

    valid, total_rows, total_columns = _extract_bundle_stats(bundle_dir)

    manifest_file = package_dir / ZIP_MANIFEST_FILE_NAME
    manifest_payload = {
        "package_id": package_id,
        "bundle_dir": bundle_dir.as_posix(),
        "zip_file": zip_file.as_posix(),
        "included_files": included_files,
        "valid": valid,
        "total_rows": total_rows,
        "total_columns": total_columns,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    _write_manifest(manifest_file, manifest_payload)

    print(f"package_id: {package_id}")
    print(f"bundle_dir: {bundle_dir.as_posix()}")
    print(f"zip_file: {zip_file.as_posix()}")
    print(f"included_files_count: {len(included_files)}")
    print(f"manifest_file: {manifest_file.as_posix()}")
    print(f"valid: {valid}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
