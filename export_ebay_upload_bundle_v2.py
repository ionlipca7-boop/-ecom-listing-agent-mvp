import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
REQUIRED_FILES = (
    "ebay_upload_ready_v2.csv",
    "ebay_upload_ready_v2_validation.json",
    "ebay_upload_ready_v2_summary.json",
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


def _copy_required_files(package_dir: Path, bundle_dir: Path) -> list[str]:
    copied_files: list[str] = []

    for file_name in REQUIRED_FILES:
        source_file = package_dir / file_name
        if not source_file.exists() or not source_file.is_file():
            raise RuntimeError(f"required file missing: {source_file.as_posix()}")

        destination_file = bundle_dir / file_name
        try:
            shutil.copy2(source_file, destination_file)
        except OSError as exc:
            raise RuntimeError(f"failed to copy file: {source_file.as_posix()}") from exc

        copied_files.append(destination_file.as_posix())

    return copied_files


def _write_manifest(manifest_file: Path, payload: dict) -> None:
    try:
        manifest_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to write manifest file: {manifest_file.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id
    bundle_dir = package_dir / "export_bundle_v2"

    bundle_dir.mkdir(parents=True, exist_ok=True)

    copied_files = _copy_required_files(package_dir, bundle_dir)

    summary_payload = _load_json_file(package_dir / "ebay_upload_ready_v2_summary.json", "summary file")
    valid = summary_payload.get("valid")
    total_rows = summary_payload.get("total_rows")
    total_columns = summary_payload.get("total_columns")

    if not isinstance(valid, bool):
        raise RuntimeError("summary valid is missing or invalid")
    if not isinstance(total_rows, int):
        raise RuntimeError("summary total_rows is missing or invalid")
    if not isinstance(total_columns, int):
        raise RuntimeError("summary total_columns is missing or invalid")

    manifest_file = bundle_dir / "export_bundle_v2_manifest.json"
    manifest_payload = {
        "package_id": package_id,
        "bundle_dir": bundle_dir.as_posix(),
        "files": copied_files,
        "valid": valid,
        "total_rows": total_rows,
        "total_columns": total_columns,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    _write_manifest(manifest_file, manifest_payload)

    print(f"package_id: {package_id}")
    print(f"bundle_dir: {bundle_dir.as_posix()}")
    print(f"files_copied: {len(copied_files)}")
    print(f"manifest_file: {manifest_file.as_posix()}")
    print(f"valid: {valid}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
