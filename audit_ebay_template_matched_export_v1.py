import argparse
import csv
import json
from pathlib import Path
from typing import Any

PUBLISH_PACKAGES_DIR = Path("publish_packages")
PUBLISH_INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
INPUT_FILENAME = "ebay_ready_for_upload_v1.csv"
AUDIT_FILENAME = "ebay_template_matched_export_v1_audit.json"
EXPECTED_COLUMNS = 96


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
    parser = argparse.ArgumentParser(description="Audit ebay_ready_for_upload_v1.csv contract before real publish.")
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


def _write_audit(path: Path, payload: dict[str, Any]) -> tuple[bool, str]:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return True, path.as_posix()
    except OSError as exc:
        return False, f"write_error: {exc}"


def main() -> int:
    args = _parse_args()

    package_id, package_error = _resolve_package_id(args.package_id)
    if not package_id:
        print("package_id: None")
        print("audit_file: unresolved")
        print("contract_ok: False")
        print("data_row_count: 0")
        print("invalid_row_count: 0")
        return 1

    package_dir = PUBLISH_PACKAGES_DIR / package_id
    input_file = package_dir / INPUT_FILENAME
    audit_file = package_dir / AUDIT_FILENAME

    row1_exists = False
    row2_exists = False
    row2_len = 0
    data_row_count = 0
    invalid_row_count = 0
    invalid_row_numbers: list[int] = []
    read_error: str | None = None

    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=";")
            row1 = next(reader, None)
            row2 = next(reader, None)

            row1_exists = row1 is not None
            row2_exists = row2 is not None
            row2_len = len(row2) if row2 is not None else 0

            current_line = 2
            for row in reader:
                current_line += 1
                if row == []:
                    continue
                data_row_count += 1
                if len(row) != EXPECTED_COLUMNS:
                    invalid_row_count += 1
                    invalid_row_numbers.append(current_line)

    except FileNotFoundError:
        read_error = "missing_input_file"
    except (csv.Error, OSError) as exc:
        read_error = f"read_error: {exc}"

    contract_ok = (
        read_error is None
        and row1_exists
        and row2_exists
        and row2_len == EXPECTED_COLUMNS
        and data_row_count >= 1
        and invalid_row_count == 0
    )

    audit_payload: dict[str, Any] = {
        "package_id": package_id,
        "input_file": input_file.as_posix(),
        "audit_file": audit_file.as_posix(),
        "row1_exists": row1_exists,
        "row2_exists": row2_exists,
        "row2_len": row2_len,
        "expected_columns": EXPECTED_COLUMNS,
        "data_row_count": data_row_count,
        "invalid_row_count": invalid_row_count,
        "invalid_row_numbers": invalid_row_numbers,
        "contract_ok": contract_ok,
    }
    if package_error:
        audit_payload["package_warning"] = package_error
    if read_error:
        audit_payload["read_error"] = read_error

    write_ok, write_info = _write_audit(audit_file, audit_payload)
    if not write_ok:
        print(json.dumps(audit_payload, ensure_ascii=False, indent=2))
        print(write_info)
        return 1

    print(f"package_id: {package_id}")
    print(f"audit_file: {audit_file.as_posix()}")
    print(f"contract_ok: {contract_ok}")
    print(f"data_row_count: {data_row_count}")
    print(f"invalid_row_count: {invalid_row_count}")
    return 0 if contract_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())