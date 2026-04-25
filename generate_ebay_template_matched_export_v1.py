import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

PUBLISH_PACKAGES_DIR = Path("publish_packages")
PUBLISH_INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
TEMPLATE_PATH = Path("templates/eBay-category-listing-template-апр.-14-2026-11-44-17.csv")
INPUT_FILENAME = "ebay_upload_ready_v2.csv"
OUTPUT_FILENAME = "ebay_ready_for_upload_v1.csv"


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
    parser = argparse.ArgumentParser(description="Generate eBay export strictly matched to eBay DE template.")
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


def _norm_key(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "", value.strip().lower())
    return cleaned


def _normalize_price(value: str) -> str | None:
    text = (value or "").strip()
    if not text:
        return None

    text = text.replace("€", "").replace(" ", "")
    text = text.replace(",", ".")
    try:
        return f"{float(text):.2f}"
    except ValueError:
        return None


def _read_template_rows(path: Path) -> tuple[bool, list[str] | None, list[str] | None, str | None]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle, delimiter=";")
            metadata_row = next(reader, None)
            header_row = next(reader, None)
    except FileNotFoundError:
        return False, None, None, "missing"
    except (csv.Error, OSError) as exc:
        return False, None, None, f"template_read_error: {exc}"

    if metadata_row is None or header_row is None:
        return False, None, None, "template_missing_required_rows"
    if not header_row:
        return False, None, None, "template_header_row_empty"

    return True, metadata_row, header_row, None


def main() -> int:
    args = _parse_args()

    package_id, package_error = _resolve_package_id(args.package_id)
    if not package_id:
        print("package_id: None")
        print("valid_rows: 0")
        print("skipped_rows: 0")
        print(f"output_path: unresolved ({package_error or 'package_resolution_failed'})")
        return 1

    package_dir = PUBLISH_PACKAGES_DIR / package_id
    input_path = package_dir / INPUT_FILENAME
    output_path = package_dir / OUTPUT_FILENAME

    template_ok, metadata_row, template_header, template_error = _read_template_rows(TEMPLATE_PATH)
    if not template_ok or metadata_row is None or template_header is None:
        print(f"package_id: {package_id}")
        print("valid_rows: 0")
        print("skipped_rows: 0")
        print(f"output_path: template_error ({template_error})")
        return 1

    valid_rows = 0
    skipped_rows = 0

    try:
        with input_path.open("r", encoding="utf-8", newline="") as in_handle:
            reader = csv.DictReader(in_handle)
            input_headers = list(reader.fieldnames or [])
            if not input_headers:
                print(f"package_id: {package_id}")
                print("valid_rows: 0")
                print("skipped_rows: 0")
                print("output_path: missing_input_headers")
                return 1

            input_by_norm = {_norm_key(h): h for h in input_headers}
            template_by_norm = [_norm_key(h) for h in template_header]

            input_has_title = "title" in input_by_norm
            input_has_price = "price" in input_by_norm
            input_has_category = "category" in input_by_norm

            exported_rows: list[list[str]] = []

            for source_row in reader:
                def pick(field_name: str) -> str:
                    key = input_by_norm.get(_norm_key(field_name))
                    return (source_row.get(key) or "").strip() if key else ""

                title = pick("title") if input_has_title else ""
                price = pick("price") if input_has_price else ""
                category = pick("category") if input_has_category else ""

                if input_has_title and not title:
                    skipped_rows += 1
                    continue
                if input_has_price and not price:
                    skipped_rows += 1
                    continue
                if input_has_category and not category:
                    skipped_rows += 1
                    continue

                normalized_price = _normalize_price(price) if input_has_price else None
                if input_has_price and normalized_price is None:
                    skipped_rows += 1
                    continue

                if input_has_title:
                    title = title[:80]

                mapped_row: list[str] = []
                for template_col, template_norm in zip(template_header, template_by_norm):
                    input_header = input_by_norm.get(template_norm)
                    value = (source_row.get(input_header) or "").strip() if input_header else ""

                    if input_has_title and template_norm == "title":
                        value = title
                    elif input_has_price and template_norm == "price":
                        value = normalized_price or ""
                    elif input_has_category and template_norm == "category":
                        value = category

                    mapped_row.append(value)

                exported_rows.append(mapped_row)
                valid_rows += 1

        package_dir.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8-sig", newline="") as out_handle:
            writer = csv.writer(out_handle, delimiter=";")
            writer.writerow(metadata_row)
            writer.writerow(template_header)
            writer.writerows(exported_rows)

    except FileNotFoundError:
        print(f"package_id: {package_id}")
        print(f"valid_rows: {valid_rows}")
        print(f"skipped_rows: {skipped_rows}")
        print(f"output_path: missing_input ({input_path.as_posix()})")
        return 1
    except (csv.Error, OSError) as exc:
        print(f"package_id: {package_id}")
        print(f"valid_rows: {valid_rows}")
        print(f"skipped_rows: {skipped_rows}")
        print(f"output_path: error ({exc})")
        return 1

    print(f"package_id: {package_id}")
    print(f"valid_rows: {valid_rows}")
    print(f"skipped_rows: {skipped_rows}")
    print(f"output_path: {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())