import json
import sys
from pathlib import Path


PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
COMPARE_FILENAME = "compare_ebay_template_vs_upload_v2.json"
MAPPING_FILENAME = "ebay_mapping_v2.json"


DIRECT_RULES = {
    "title": "*Title",
    "description": "*Description",
    "price": "*StartPrice",
    "quantity": "*Quantity",
    "duration": "*Duration",
    "format": "*Format",
}

TRANSFORM_RULES = {
    "category": "*Category",
    "condition": "*ConditionID",
}

STATIC_DEFAULT_RULES = {
    "*Format": "FixedPrice",
    "*Duration": "GTC",
    "*Location": "Germany",
}


def _load_json_object(file_path: Path, context: str) -> dict:
    try:
        payload = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"failed to read {context}: {file_path.as_posix()}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError(f"{context} must be a JSON object: {file_path.as_posix()}")

    return payload


def _load_latest_package_id() -> str:
    if INDEX_PATH.exists() and INDEX_PATH.is_file():
        payload = _load_json_object(INDEX_PATH, "publish index")
        latest_package = payload.get("latest_package")
        if isinstance(latest_package, str) and latest_package.strip():
            return latest_package.strip()

    if not PUBLISH_PACKAGES_DIR.exists() or not PUBLISH_PACKAGES_DIR.is_dir():
        raise RuntimeError(f"publish packages directory not found: {PUBLISH_PACKAGES_DIR.as_posix()}")

    package_dirs = sorted(
        [
            path.name
            for path in PUBLISH_PACKAGES_DIR.iterdir()
            if path.is_dir() and path.name.startswith("package_")
        ]
    )

    if not package_dirs:
        raise RuntimeError("no package_* directories found in publish_packages")

    return package_dirs[-1]


def _load_compare_payload(package_dir: Path) -> dict:
    compare_file = package_dir / COMPARE_FILENAME

    if not compare_file.exists() or not compare_file.is_file():
        raise RuntimeError(f"compare file not found: {compare_file.as_posix()}")

    payload = _load_json_object(compare_file, "compare report")

    required_keys = [
        "package_id",
        "upload_only_columns",
        "template_only_columns",
        "common_columns",
    ]
    missing = [key for key in required_keys if key not in payload]
    if missing:
        raise RuntimeError(f"compare report missing keys: {', '.join(missing)}")

    return payload


def _ensure_string_list(value: object, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise RuntimeError(f"{field_name} must be a list")

    cleaned: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise RuntimeError(f"{field_name} must contain only strings")
        text = item.strip()
        if text:
            cleaned.append(text)

    return cleaned


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _build_mapping(compare_payload: dict) -> dict:
    upload_only_columns = _ensure_string_list(compare_payload.get("upload_only_columns"), "upload_only_columns")
    template_only_columns = _ensure_string_list(compare_payload.get("template_only_columns"), "template_only_columns")
    common_columns = _ensure_string_list(compare_payload.get("common_columns"), "common_columns")

    upload_columns = _dedupe_preserve_order(upload_only_columns + common_columns)
    template_columns = _dedupe_preserve_order(common_columns + template_only_columns)

    template_set = set(template_columns)
    upload_set = set(upload_columns)

    direct_map = {
        source: target
        for source, target in DIRECT_RULES.items()
        if source in upload_set and target in template_set
    }

    transform_map = {
        source: target
        for source, target in TRANSFORM_RULES.items()
        if source in upload_set and target in template_set
    }

    claimed_template_fields = set(direct_map.values()) | set(transform_map.values())

    static_defaults = {
        field: value
        for field, value in STATIC_DEFAULT_RULES.items()
        if field in template_set and field not in claimed_template_fields
    }

    claimed_template_fields |= set(static_defaults.keys())

    empty_fields = [field for field in template_columns if field not in claimed_template_fields]

    return {
        "upload_columns": upload_columns,
        "template_columns": template_columns,
        "direct_map": direct_map,
        "transform_map": transform_map,
        "static_defaults": static_defaults,
        "empty_fields": empty_fields,
    }


def _write_json(file_path: Path, payload: dict) -> None:
    try:
        file_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError as exc:
        raise RuntimeError(f"failed to write mapping file: {file_path.as_posix()}") from exc


def main() -> int:
    package_id = _load_latest_package_id()
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    if not package_dir.exists() or not package_dir.is_dir():
        raise RuntimeError(f"package directory not found: {package_dir.as_posix()}")

    compare_payload = _load_compare_payload(package_dir)
    mapping_payload = _build_mapping(compare_payload)

    output_payload = {
        "package_id": package_id,
        "direct_map": mapping_payload["direct_map"],
        "transform_map": mapping_payload["transform_map"],
        "static_defaults": mapping_payload["static_defaults"],
        "empty_fields": mapping_payload["empty_fields"],
        "meta": {
            "upload_columns": mapping_payload["upload_columns"],
            "template_columns": mapping_payload["template_columns"],
        },
    }

    mapping_file = package_dir / MAPPING_FILENAME
    _write_json(mapping_file, output_payload)

    mapped_fields_count = (
        len(output_payload["direct_map"])
        + len(output_payload["transform_map"])
        + len(output_payload["static_defaults"])
    )

    print(f"package_id: {package_id}")
    print(f"total_template_fields: {len(mapping_payload['template_columns'])}")
    print(f"mapped_fields_count: {mapped_fields_count}")
    print(f"empty_fields_count: {len(output_payload['empty_fields'])}")
    print(f"mapping_file: {mapping_file.as_posix()}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)