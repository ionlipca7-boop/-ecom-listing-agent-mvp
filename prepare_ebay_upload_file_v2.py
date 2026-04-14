import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
TEMPLATES_DIR = Path("templates")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
TEMPLATE_PATH = TEMPLATES_DIR / "ebay_category_template.csv"


ALIASES = {
    "*action(s=siteid|country|currency|version|ccode)": [
        "action(s=siteid|country|currency|version|ccode)"
    ],
    "*category": ["category"],
    "*conditionid": ["conditionid", "condition id"],
    "*c:brand": ["brand", "c:brand"],
    "*format": ["format"],
    "*quantity": ["quantity", "qty"],
    "*title": ["title"],
    "*startprice": ["startprice", "start price", "price"],
    "*description": ["description", "html description"],
    "*duration": ["duration"],
    "*dispatchtimemax": ["dispatchtimemax", "dispatch time max"],
    "*returnsacceptedoption": ["returnsacceptedoption", "returns accepted"],
    "*returnspolicyoption": ["returnspolicyoption", "returns policy"],
    "*shippingtype": ["shippingtype", "shipping type"],
    "*location": ["location"],
    "*postalcode": ["postalcode", "zip", "zipcode"],
    "*country": ["country"],
    "*picurl": ["picurl", "picture urls", "image urls"],
    "*upc": ["upc"],
    "*ean": ["ean"],
    "*mpn": ["mpn"],
    "*sku": ["sku"],
}


def _normalize(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def _load_latest_package_id(index_path: Path) -> str:
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read index file: {index_path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("publish index must be a JSON object")

    latest_package = payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        raise RuntimeError("latest_package is missing in publish index")

    return latest_package


def _read_template_columns(template_path: Path) -> list[str]:
    try:
        with template_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            first_row = next(reader, None)
    except OSError as exc:
        raise RuntimeError(f"failed to read template CSV: {template_path.as_posix()}") from exc

    if not first_row:
        raise RuntimeError("template CSV is empty")
    return first_row


def _load_source_rows(input_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise RuntimeError("input CSV has no header")
            rows = list(reader)
            return list(reader.fieldnames), rows
    except OSError as exc:
        raise RuntimeError(f"failed to read input CSV: {input_path.as_posix()}") from exc


def _build_source_lookup(source_columns: list[str]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for col in source_columns:
        lookup[_normalize(col)] = col
    return lookup


def _resolve_source_column(template_col: str, source_lookup: dict[str, str]) -> str | None:
    direct = source_lookup.get(_normalize(template_col))
    if direct:
        return direct

    for alias in ALIASES.get(template_col, []):
        candidate = source_lookup.get(_normalize(alias))
        if candidate:
            return candidate

    wildcard_name = template_col.replace("*", "")
    if wildcard_name:
        candidate = source_lookup.get(_normalize(wildcard_name))
        if candidate:
            return candidate

    return None


def _map_rows_to_template(
    template_columns: list[str], source_columns: list[str], source_rows: list[dict[str, str]]
) -> tuple[list[dict[str, str]], list[str]]:
    source_lookup = _build_source_lookup(source_columns)
    mapped_columns: dict[str, str | None] = {
        template_col: _resolve_source_column(template_col, source_lookup)
        for template_col in template_columns
    }

    unmapped_required = [
        col for col, source_col in mapped_columns.items() if source_col is None and col.startswith("*")
    ]

    output_rows: list[dict[str, str]] = []
    for row in source_rows:
        out_row: dict[str, str] = {}
        for template_col in template_columns:
            source_col = mapped_columns[template_col]
            out_row[template_col] = row.get(source_col, "") if source_col else ""
        output_rows.append(out_row)

    return output_rows, unmapped_required


def _write_output(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    try:
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        raise RuntimeError(f"failed to write output CSV: {path.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    input_file = package_dir / "ebay_feed_final.csv"
    output_file = package_dir / "ebay_upload_ready_v2.csv"

    template_columns = _read_template_columns(TEMPLATE_PATH)
    source_columns, source_rows = _load_source_rows(input_file)
    output_rows, unmapped_required = _map_rows_to_template(
        template_columns, source_columns, source_rows
    )
    _write_output(output_file, template_columns, output_rows)

    print(f"package_id: {package_id}")
    print(f"template_file: {TEMPLATE_PATH.as_posix()}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"output_file: {output_file.as_posix()}")
    print(f"total_items: {len(output_rows)}")
    if unmapped_required:
        print("warning_unmapped_required_columns: " + ", ".join(unmapped_required))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
