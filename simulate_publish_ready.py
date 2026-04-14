import json
from datetime import datetime, timezone
from pathlib import Path


HISTORY_DIR = Path("history")
PUBLISH_LOGS_DIR = Path("publish_logs")


def _record_sort_key(record, path):
    timestamp = record.get("timestamp") if isinstance(record, dict) else None
    if isinstance(timestamp, str):
        try:
            return datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        except ValueError:
            pass

    stem = path.stem
    core = stem[4:] if stem.startswith("run_") else stem
    parts = core.split("_")
    if len(parts) >= 2:
        token = f"{parts[0]}_{parts[1]}"
        try:
            return datetime.strptime(token, "%Y%m%d_%H%M%S")
        except ValueError:
            pass

    return datetime.fromtimestamp(path.stat().st_mtime)


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


def _normalize_status(value):
    if not isinstance(value, str) or not value.strip():
        return "review"

    status = value.strip().lower()
    if status == "draft":
        return "review"
    return status


def _read_run_row(path, record):
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

    return {
        "file_name": path.name,
        "approval_status": approval_status,
        "publish_ready": publish_ready,
    }


def _load_rows(history_dir):
    rows = []
    for path in history_dir.glob("run_*.json"):
        if not path.is_file():
            continue
        try:
            with path.open("r", encoding="utf-8") as f:
                record = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue

        rows.append(
            (
                _record_sort_key(record, path),
                _read_run_row(path, record),
                record,
                path,
            )
        )

    rows.sort(key=lambda item: item[0], reverse=True)
    return rows


def _apply_publish_ready_filter(row_entries):
    return [entry for entry in row_entries if entry[1]["publish_ready"]]


def _extract_simulated_item(path, record):
    previous_publish_status = _pick_field(
        record,
        ("listing_result", "publish_status"),
        ("pipeline_summary", "publish_status"),
        ("listing_result", "status"),
        ("pipeline_summary", "status"),
    )

    return {
        "source_run_file": path.name,
        "title": _pick_field(
            record,
            ("listing_result", "title"),
            ("parsed_product", "title"),
            ("parsed_product", "product_name"),
            ("parsed_product", "query"),
            ("raw_input",),
        ),
        "category": _pick_field(
            record,
            ("listing_result", "category"),
            ("parsed_product", "category"),
        ),
        "price": _pick_field(
            record,
            ("listing_result", "price"),
            ("parsed_product", "price"),
        ),
        "previous_publish_status": previous_publish_status,
        "simulated_publish_status": "published_simulated",
        "simulated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
    }


def main():
    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        rows = []
    else:
        rows = _load_rows(HISTORY_DIR)
    publish_ready_rows = _apply_publish_ready_filter(rows)

    simulated_items = [
        _extract_simulated_item(path, record)
        for _, _, record, path in publish_ready_rows
    ]

    PUBLISH_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_file = PUBLISH_LOGS_DIR / f"publish_simulation_{timestamp}.json"

    output_payload = {
        "timestamp": timestamp,
        "scanned": len(rows),
        "simulated": len(simulated_items),
        "results": simulated_items,
    }

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    print(f"scanned: {len(rows)}")
    print(f"simulated: {len(simulated_items)}")
    print(f"output_file: {output_file.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
