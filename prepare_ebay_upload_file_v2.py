import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
EXACT_TEMPLATE_PATH = Path("templates/ebay_category_template.csv")
TEMPLATE_DIR = Path("templates")
FALLBACK_KEYWORDS = ("ebay", "template", "category")


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


def _resolve_template_path() -> Path:
    if EXACT_TEMPLATE_PATH.is_file():
        return EXACT_TEMPLATE_PATH

    if not TEMPLATE_DIR.is_dir():
        raise RuntimeError(
            "template not found: templates/ebay_category_template.csv; "
            "fallback search skipped because templates directory is missing"
        )

    fallback_candidates: list[Path] = []
    for candidate in sorted(TEMPLATE_DIR.iterdir(), key=lambda path: path.name.lower()):
        if not candidate.is_file() or candidate.suffix.lower() != ".csv":
            continue

        lower_name = candidate.name.lower()
        if any(keyword in lower_name for keyword in FALLBACK_KEYWORDS):
            fallback_candidates.append(candidate)

    if fallback_candidates:
        return fallback_candidates[0]

    raise RuntimeError(
        "template not found: templates/ebay_category_template.csv; "
        "no fallback CSV matched keywords ebay/template/category in templates/"
    )


def _read_template_fieldnames(template_path: Path) -> list[str]:
    try:
        with template_path.open("r", encoding="utf-8-sig", newline="") as src:
            reader = csv.DictReader(src)
            fieldnames = reader.fieldnames
    except OSError as exc:
        raise RuntimeError(f"failed to read template CSV: {template_path.as_posix()}") from exc

    if not fieldnames:
        raise RuntimeError(f"template CSV has no header: {template_path.as_posix()}")

    return fieldnames


def _copy_csv_using_template_schema(input_file: Path, output_file: Path, fieldnames: list[str]) -> int:
    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as src:
            reader = csv.DictReader(src)
            input_rows = list(reader)
    except OSError as exc:
        raise RuntimeError(f"failed to read input CSV: {input_file.as_posix()}") from exc

    normalized_rows: list[dict[str, str]] = []
    for row in input_rows:
        normalized_rows.append({name: row.get(name, "") for name in fieldnames})

    try:
        with output_file.open("w", encoding="utf-8-sig", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(normalized_rows)
    except OSError as exc:
        raise RuntimeError(f"failed to write output CSV: {output_file.as_posix()}") from exc

    return len(normalized_rows)


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    input_file = package_dir / "ebay_feed_final.csv"
    output_file = package_dir / "ebay_upload_ready.csv"

    template_file = _resolve_template_path()
    template_fieldnames = _read_template_fieldnames(template_file)
    total_items = _copy_csv_using_template_schema(input_file, output_file, template_fieldnames)

    print(f"package_id: {package_id}")
    print(f"template_file: {template_file.as_posix()}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"output_file: {output_file.as_posix()}")
    print(f"total_items: {total_items}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
