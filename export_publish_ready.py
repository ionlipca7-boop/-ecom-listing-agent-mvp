import json
from pathlib import Path


HISTORY_DIR = Path("history")
OUTPUT_PATH = Path("exports") / "publish_ready_export.json"


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


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


def _normalize_status(value):
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


def _extract_export_row(record, source_name):
    approval_status = _normalize_status(
        _pick_field(
            record,
            ("listing_result", "approval_status"),
            ("pipeline_summary", "approval_status"),
            ("listing_result", "control_status"),
            ("pipeline_summary", "control_status"),
            ("listing_result", "status"),
            ("pipeline_summary", "status"),
        )
    )

    publish_ready = approval_status == "publish_ready"
    quality_gate_ready = _to_bool(
        _pick_field(
            record,
            ("listing_result", "quality_gate_ready"),
            ("pipeline_summary", "quality_gate_ready"),
            ("listing_result", "publish_ready"),
            ("pipeline_summary", "publish_ready"),
        )
    )

    if not publish_ready:
        return None

    return {
        "source_run_file": source_name,
        "title": _pick_field(record, ("listing_result", "title")),
        "category": _pick_field(
            record,
            ("listing_result", "category"),
            ("listing_result", "category_path"),
        ),
        "price": _pick_field(record, ("listing_result", "price")),
        "description": _pick_field(record, ("listing_result", "description")),
        "item_specifics": _pick_field(record, ("listing_result", "item_specifics")),
        "approval_status": approval_status,
        "publish_ready": publish_ready,
        "quality_gate_ready": quality_gate_ready,
    }


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    scanned = 0
    exported_rows = []

    if HISTORY_DIR.exists() and HISTORY_DIR.is_dir():
        for run_file in sorted(HISTORY_DIR.glob("run_*.json")):
            if not run_file.is_file():
                continue
            scanned += 1
            try:
                with run_file.open("r", encoding="utf-8") as f:
                    record = json.load(f)
            except (OSError, json.JSONDecodeError):
                continue

            row = _extract_export_row(record, run_file.name)
            if row is not None:
                exported_rows.append(row)

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(exported_rows, f, ensure_ascii=False, indent=2)

    print(f"scanned: {scanned}")
    print(f"exported: {len(exported_rows)}")
    print(f"output_path: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
