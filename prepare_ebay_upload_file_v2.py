import csv
import json
from pathlib import Path

PUBLISH_PACKAGES_DIR = Path("publish_packages")
TEMPLATES_DIR = Path("templates")
INDEX_PATH = PUBLISH_PACKAGES_DIR / "publish_index.json"
TEMPLATE_DELIMITER_CANDIDATES = (",", "\t", ";", "|")


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


def _resolve_template_file(templates_dir: Path) -> Path:
    template_candidates = sorted(
        templates_dir.glob("eBay-category-listing-template*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if template_candidates:
        return template_candidates[0]

    fallback_candidates = sorted(
        templates_dir.glob("*.csv"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if fallback_candidates:
        return fallback_candidates[0]

    raise RuntimeError(f"no CSV template files found in: {templates_dir.as_posix()}")


def _score_template_row(cells: list[str], delimiter: str) -> tuple[int, int, int, int]:
    non_empty_cells = [cell for cell in cells if cell.strip()]
    width = len(cells)
    non_empty_width = len(non_empty_cells)
    unique_non_empty_width = len(set(non_empty_cells))
    preferred_delimiter = 1 if delimiter == "," else 0
    return (width, non_empty_width, unique_non_empty_width, preferred_delimiter)


def _detect_template_header(csv_file: Path) -> list[str]:
    try:
        lines = csv_file.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        raise RuntimeError(f"failed to read template CSV: {csv_file.as_posix()}") from exc

    best_header: list[str] = []
    best_score = (-1, -1, -1, -1)

    for line in lines:
        if not line.strip():
            continue

        for delimiter in TEMPLATE_DELIMITER_CANDIDATES:
            cells = next(csv.reader([line], delimiter=delimiter))
            cleaned_cells = [str(cell).strip() for cell in cells]
            score = _score_template_row(cleaned_cells, delimiter)
            if score > best_score:
                best_header = cleaned_cells
                best_score = score

    if not best_header:
        raise RuntimeError(f"template CSV has no usable header: {csv_file.as_posix()}")

    return best_header


def _normalize_column_name(name: str) -> str:
    return str(name).strip().casefold()


def _build_template_ordered_row(
    input_row: dict[str, str],
    input_index: dict[str, str],
    template_header: list[str],
) -> dict[str, str]:
    mapped_row: dict[str, str] = {}
    for template_col in template_header:
        source_col = input_index.get(_normalize_column_name(template_col))
        mapped_row[template_col] = input_row.get(source_col, "") if source_col else ""
    return mapped_row


def _write_template_aligned_csv(input_file: Path, template_header: list[str], output_file: Path) -> int:
    try:
        with input_file.open("r", encoding="utf-8-sig", newline="") as src:
            reader = csv.DictReader(src)
            fieldnames = reader.fieldnames
            if not fieldnames:
                raise RuntimeError("input CSV has no header")

            input_index = {_normalize_column_name(name): name for name in fieldnames}
            rows = [
                _build_template_ordered_row(input_row=row, input_index=input_index, template_header=template_header)
                for row in reader
            ]
    except OSError as exc:
        raise RuntimeError(f"failed to read input CSV: {input_file.as_posix()}") from exc

    try:
        with output_file.open("w", encoding="utf-8-sig", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=template_header)
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        raise RuntimeError(f"failed to write output CSV: {output_file.as_posix()}") from exc

    return len(rows)


def main() -> int:
    package_id = _load_latest_package_id(INDEX_PATH)
    package_dir = PUBLISH_PACKAGES_DIR / package_id

    template_file = _resolve_template_file(TEMPLATES_DIR)
    template_header = _detect_template_header(template_file)
    input_file = package_dir / "ebay_feed_final.csv"
    output_file = package_dir / "ebay_upload_ready_v2.csv"

    total_items = _write_template_aligned_csv(input_file, template_header, output_file)

    print(f"package_id: {package_id}")
    print(f"template_file: {template_file.as_posix()}")
    print(f"input_file: {input_file.as_posix()}")
    print(f"output_file: {output_file.as_posix()}")
    print(f"total_items: {total_items}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
