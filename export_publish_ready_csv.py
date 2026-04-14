import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from list_queue import HISTORY_DIR, _apply_filter, _load_rows


EXPORTS_DIR = Path("exports")
CSV_COLUMNS = [
    "source_run_file",
    "title",
    "category",
    "price",
    "description",
    "approval_status",
    "publish_status",
    "quality_gate_ready",
]


def _build_output_path() -> Path:
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    return EXPORTS_DIR / f"publish_ready_{timestamp}.csv"


def _pick_field(record, *paths):
    for path in paths:
        value = record
        found = True
        for key in path:
            if not isinstance(value, dict) or key not in value:
                found = False
                break
            value = value[key]
        if found:
            return value
    return None


def _normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _normalize_bool(value):
    return "true" if bool(value) else "false"


def _row_to_csv_record(run_file: str, record: dict) -> dict:
    return {
        "source_run_file": run_file,
        "title": _normalize_text(
            _pick_field(
                record,
                ("listing_result", "title"),
                ("parsed_product", "title"),
                ("parsed_product", "product_name"),
            )
        ),
        "category": _normalize_text(
            _pick_field(
                record,
                ("listing_result", "category"),
                ("parsed_product", "category"),
            )
        ),
        "price": _normalize_text(
            _pick_field(
                record,
                ("listing_result", "price"),
                ("parsed_product", "price"),
            )
        ),
        "description": _normalize_text(
            _pick_field(
                record,
                ("listing_result", "description"),
                ("parsed_product", "description"),
            )
        ),
        "approval_status": _normalize_text(
            _pick_field(
                record,
                ("listing_result", "approval_status"),
                ("pipeline_summary", "approval_status"),
            )
        ),
        "publish_status": _normalize_text(
            _pick_field(
                record,
                ("publish_result", "status"),
                ("pipeline_summary", "publish_status"),
            )
        ),
        "quality_gate_ready": _normalize_bool(
            _pick_field(
                record,
                ("listing_result", "quality_gate_ready"),
                ("pipeline_summary", "quality_gate_ready"),
            )
        ),
    }


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    output_path = _build_output_path()

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        _write_csv(output_path, [])
        print("scanned: 0")
        print("exported: 0")
        print(f"output_file: {output_path}")
        return 0

    queue_rows = _load_rows(HISTORY_DIR)
    publish_ready_rows = _apply_filter(queue_rows, "publish_ready")

    csv_rows = []
    for row in publish_ready_rows:
        run_file = row["file_name"]
        run_path = HISTORY_DIR / run_file
        try:
            with run_path.open("r", encoding="utf-8") as f:
                record = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue

        csv_rows.append(_row_to_csv_record(run_file, record))

    _write_csv(output_path, csv_rows)

    print(f"scanned: {len(queue_rows)}")
    print(f"exported: {len(csv_rows)}")
    print(f"output_file: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
