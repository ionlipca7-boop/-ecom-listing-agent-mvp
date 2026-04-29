import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
COMPARE_FILE_NAME = "compare_ebay_template_vs_upload_v2.json"
MAPPING_FILE_NAME = "ebay_mapping_v2.json"

DIRECT_MAP_RULES = {
    "title": "*Title",
    "description": "*Description",
    "price": "*StartPrice",
    "quantity": "*Quantity",
    "duration": "*Duration",
    "format": "*Format",
}

TRANSFORM_MAP_RULES = {
    "category": "*Category",
    "condition": "*ConditionID",
}

STATIC_DEFAULTS_RULES = {
    "*Format": "FixedPrice",
    "*Duration": "GTC",
    "*Location": "Germany",
    "*Country": "DE",
    "*Currency": "EUR",
}


def _load_json_file(path: Path, context: str) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read {context}: {path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError(f"{context} must be a JSON object")

    return payload


def _load_latest_package_id() -> str:
    if INDEX_PATH.exists() and INDEX_PATH.is_file():
        payload = _load_json_file(INDEX_PATH, "publish index")
        latest_package = payload.get("latest_package")
        if isinstance(latest_package, str) and latest_package:
            return latest_package

    if not PUBLISH_PACKAGES_DIR.exists() or not PUBLISH_PACKAGES_DIR.is_dir():
        raise RuntimeError("publish_packages directory is missing")

    package_dirs = sorted(
        [path for path in PUBLISH_PACKAGES_DIR.glob("package_*") if path.is_dir()],
        key=lambda item: item.name,
    )
    if not package_dirs:
        raise RuntimeError("no package directories found")

    return package_dirs[-1].name


def _normalize_column(item: object) -> str | None:
    if isinstance(item, str):
        value = item.strip()
        return value if value else None

    if isinstance(item, dict):
        for key in ("column", "name", "field", "header"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    return None


def _extract_columns(payload: dict, key: str) -> list[str]:
    raw_columns = payload.get(key)
    if not isinstance(raw_columns, list):
        raise RuntimeError(f"{key} must be a list")

    columns: list[str] = []
    seen: set[str] = set()
    for item in raw_columns:
        column = _normalize_column(item)
        if column is None or column in seen:
            continue
        seen.add(column)
        columns.append(column)

    return columns


def _build_filtered_map(rules: dict[str, str], upload_columns: set[str], template_columns: set[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for source_field, target_field in rules.items():
        if source_field in upload_columns and target_field in template_columns:
            result[source_field] = target_field
    return result


def _build_mapping(upload_columns: list[str], template_columns: list[str]) -> dict:
    upload_set = set(upload_columns)
    template_set = set(template_columns)

    direct_map = _build_filtered_map(DIRECT_MAP_RULES, upload_set, template_set)
    transform_map = _build_filtered_map(TRANSFORM_MAP_RULES, upload_set, template_set)

    static_defaults: dict[str, str] = {}
    for target_field, value in STATIC_DEFAULTS_RULES.items():
        if target_field in template_set:
            static_defaults[target_field] = value

    mapped_targets = set(direct_map.values()) | set(transform_map.values()) | set(static_defaults.keys())
    empty_fields = [field for field in template_columns if field not in mapped_targets]

    return {
        "direct_map": direct_map,
        "transform_map": transform_map,
        "static_defaults": static_defaults,
        "empty_fields": empty_fields,
    }


def main() -> int:
    package_id = _load_latest_package_id()
    package_dir = PUBLISH_PACKAGES_DIR / package_id
    compare_file = package_dir / COMPARE_FILE_NAME

    compare_payload = _load_json_file(compare_file, "compare file")
    upload_columns = _extract_columns(compare_payload, "upload_columns")
    template_columns = _extract_columns(compare_payload, "template_columns")

    mapping_payload = _build_mapping(upload_columns, template_columns)
    mapping_file = package_dir / MAPPING_FILE_NAME
    mapping_file.write_text(json.dumps(mapping_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    mapped_fields_count = len(
        set(mapping_payload["direct_map"].values())
        | set(mapping_payload["transform_map"].values())
        | set(mapping_payload["static_defaults"].keys())
    )
    empty_fields_count = len(mapping_payload["empty_fields"])

    print(f"package_id: {package_id}")
    print(f"total_template_fields: {len(template_columns)}")
    print(f"mapped_fields_count: {mapped_fields_count}")
    print(f"empty_fields_count: {empty_fields_count}")
    print(f"mapping_file: {mapping_file.as_posix()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
