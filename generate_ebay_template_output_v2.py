import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
SOURCE_FILENAME = "ebay_upload_ready_v2.csv"
MAPPING_FILENAME = "ebay_mapping_v2.json"
OUTPUT_FILENAME = "ebay_template_output_v2.csv"


def _load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read json file: {path.as_posix()}") from exc


def _load_latest_package_id(index_path: Path) -> str:
    payload = _load_json(index_path)
    if not isinstance(payload, dict):
        raise RuntimeError("publish index must be a JSON object")

    latest_package = payload.get("latest_package")
    if not isinstance(latest_package, str) or not latest_package:
        raise RuntimeError("latest_package is missing in publish index")

    return latest_package


def _load_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            header = [str(column) for column in (reader.fieldnames or [])]
            if not header:
                raise RuntimeError(f"csv file has empty header: {path.as_posix()}")
            rows = [{str(key): (value if value is not None else "") for key, value in row.items()} for row in reader]
    except OSError as exc:
        raise RuntimeError(f"failed to read csv file: {path.as_posix()}") from exc

    return header, rows


def _mapping_meta(mapping_payload: object) -> dict:
    if not isinstance(mapping_payload, dict):
        raise RuntimeError("mapping file must be a JSON object")

    meta = mapping_payload.get("meta")
    if isinstance(meta, dict):
        return meta

    return mapping_payload


def _normalize_map(mapping_obj: object) -> dict[str, str]:
    if not isinstance(mapping_obj, dict):
        return {}

    normalized: dict[str, str] = {}
    for key, value in mapping_obj.items():
        if isinstance(key, str) and isinstance(value, str):
            normalized[key] = value
    return normalized


def _build_target_to_source_maps(
    source_header: list[str],
    template_columns: list[str],
    direct_map: dict[str, str],
    transform_map: dict[str, str],
) -> tuple[dict[str, str], dict[str, str]]:
    source_set = set(source_header)
    template_set = set(template_columns)

    direct_target_to_source: dict[str, str] = {}
    transform_target_to_source: dict[str, str] = {}

    for left, right in direct_map.items():
        if left in source_set and right in template_set:
            direct_target_to_source[right] = left
        elif right in source_set and left in template_set:
            direct_target_to_source[left] = right

    for left, right in transform_map.items():
        if left in source_set and right in template_set:
            transform_target_to_source[right] = left
        elif right in source_set and left in template_set:
            transform_target_to_source[left] = right

    return direct_target_to_source, transform_target_to_source


def _build_output_rows(
    source_rows: list[dict[str, str]],
    template_columns: list[str],
    direct_target_to_source: dict[str, str],
    transform_target_to_source: dict[str, str],
    static_defaults: dict[str, str],
    empty_fields: set[str],
) -> list[dict[str, str]]:
    output_rows: list[dict[str, str]] = []

    for source_row in source_rows:
        output_row: dict[str, str] = {}
        for column in template_columns:
            value = ""

            if column in direct_target_to_source:
                value = source_row.get(direct_target_to_source[column], "")
            elif column in transform_target_to_source:
                value = source_row.get(transform_target_to_source[column], "")
            elif column in static_defaults:
                value = static_defaults[column]
            elif column in empty_fields:
                value = ""

            output_row[column] = value

        output_rows.append(output_row)

    return output_rows


def _write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    try:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        raise RuntimeError(f"failed to write csv file: {path.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    source_file = package_dir / SOURCE_FILENAME
    mapping_file = package_dir / MAPPING_FILENAME
    output_file = package_dir / OUTPUT_FILENAME

    source_header, source_rows = _load_csv_rows(source_file)
    mapping_payload = _load_json(mapping_file)
    meta = _mapping_meta(mapping_payload)

    template_columns_raw = meta.get("template_columns") if isinstance(meta, dict) else None
    if not isinstance(template_columns_raw, list) or not all(isinstance(item, str) for item in template_columns_raw):
        raise RuntimeError("template_columns is missing or invalid in mapping meta")
    template_columns = [str(item) for item in template_columns_raw]

    direct_map = _normalize_map(meta.get("direct_map"))
    transform_map = _normalize_map(meta.get("transform_map"))
    static_defaults = _normalize_map(meta.get("static_defaults"))

    empty_fields_raw = meta.get("empty_fields") if isinstance(meta, dict) else None
    empty_fields = set()
    if isinstance(empty_fields_raw, list):
        empty_fields = {item for item in empty_fields_raw if isinstance(item, str)}

    direct_target_to_source, transform_target_to_source = _build_target_to_source_maps(
        source_header=source_header,
        template_columns=template_columns,
        direct_map=direct_map,
        transform_map=transform_map,
    )

    output_rows = _build_output_rows(
        source_rows=source_rows,
        template_columns=template_columns,
        direct_target_to_source=direct_target_to_source,
        transform_target_to_source=transform_target_to_source,
        static_defaults=static_defaults,
        empty_fields=empty_fields,
    )

    _write_csv(output_file, template_columns, output_rows)

    print(f"package_id: {package_id}")
    print(f"source_rows: {len(source_rows)}")
    print(f"output_columns: {len(template_columns)}")
    print(f"output_file: {output_file.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
