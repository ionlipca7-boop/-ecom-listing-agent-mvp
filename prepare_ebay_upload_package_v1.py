import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PUBLISH_PACKAGES_DIR = Path("publish_packages")
PUBLISH_INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
SOURCE_CSV_NAME = "ebay_ready_for_upload_v1.csv"
AUDIT_JSON_NAME = "ebay_template_matched_export_v1_audit.json"
OUTPUT_DIR_NAME = "ebay_upload_package_v1"
MANIFEST_NAME = "manifest.json"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _safe_read_json(path: Path) -> tuple[bool, Any | None, str | None]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return True, payload, None
    except FileNotFoundError:
        return False, None, "missing"
    except json.JSONDecodeError as exc:
        return False, None, f"invalid_json: {exc}"
    except OSError as exc:
        return False, None, f"read_error: {exc}"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare final eBay upload package v1.")
    parser.add_argument("--package", dest="package_id", help="Specific package id under publish_packages/")
    return parser.parse_args()


def _resolve_package_id(explicit_package_id: str | None) -> tuple[str | None, str | None]:
    if explicit_package_id and explicit_package_id.strip():
        return explicit_package_id.strip(), None

    ok, payload, error = _safe_read_json(PUBLISH_INDEX_PATH)
    if not ok:
        if error == "missing":
            return None, "publish_index_missing"
        return None, f"publish_index_invalid ({error})"

    if not isinstance(payload, dict):
        return None, "publish_index_invalid (root_not_object)"

    latest_package = payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package.strip():
        return None, "latest_package_missing"

    return latest_package.strip(), None


def main() -> int:
    args = _parse_args()

    package_id, package_error = _resolve_package_id(args.package_id)
    if not package_id:
        print("package_id: None")
        print("output_dir: unresolved")
        print("files_copied: 0")
        print("status: BLOCKED")
        return 1

    package_dir = PUBLISH_PACKAGES_DIR / package_id
    source_csv = package_dir / SOURCE_CSV_NAME
    audit_file = package_dir / AUDIT_JSON_NAME

    if not audit_file.exists():
        print(f"package_id: {package_id}")
        print("output_dir: unresolved")
        print("files_copied: 0")
        print("status: BLOCKED")
        return 1

    ok, audit_payload, audit_error = _safe_read_json(audit_file)
    if not ok or not isinstance(audit_payload, dict):
        print(f"package_id: {package_id}")
        print("output_dir: unresolved")
        print("files_copied: 0")
        print("status: BLOCKED")
        return 1

    contract_ok = bool(audit_payload.get("contract_ok") is True)
    if not contract_ok:
        print(f"package_id: {package_id}")
        print("output_dir: unresolved")
        print("files_copied: 0")
        print("status: BLOCKED")
        return 1

    if not source_csv.exists():
        print(f"package_id: {package_id}")
        print("output_dir: unresolved")
        print("files_copied: 0")
        print("status: BLOCKED")
        return 1

    output_dir = package_dir / OUTPUT_DIR_NAME
    output_csv = output_dir / SOURCE_CSV_NAME
    output_audit = output_dir / AUDIT_JSON_NAME
    manifest_path = output_dir / MANIFEST_NAME

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_csv, output_csv)
        shutil.copy2(audit_file, output_audit)

        manifest_payload = {
            "package_id": package_id,
            "status": "READY_FOR_UPLOAD",
            "source_csv": source_csv.as_posix(),
            "audit_file": audit_file.as_posix(),
            "created_at": _utc_now(),
        }
        manifest_path.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    except OSError:
        print(f"package_id: {package_id}")
        print(f"output_dir: {output_dir.as_posix()}")
        print("files_copied: 0")
        print("status: BLOCKED")
        return 1

    print(f"package_id: {package_id}")
    print(f"output_dir: {output_dir.as_posix()}")
    print("files_copied: 2")
    print("status: READY_FOR_UPLOAD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())