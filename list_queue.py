import json
import sys
from datetime import datetime
from pathlib import Path


HISTORY_DIR = Path("history")
SUPPORTED_FILTERS = {"review", "approved", "publish_ready"}
DEFAULT_LIMIT = 15


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


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
    query = _pick_field(
        record,
        ("raw_input",),
        ("parsed_product", "product_name"),
        ("parsed_product", "query"),
        ("parsed_product", "title"),
        ("listing_result", "title"),
    )
    if query is None:
        query = "-"

    status = _pick_field(
        record,
        ("listing_result", "status"),
        ("pipeline_summary", "status"),
    )
    if not isinstance(status, str) or not status.strip():
        status = "-"

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

    quality_gate_ready = _to_bool(
        _pick_field(
            record,
            ("listing_result", "quality_gate_ready"),
            ("pipeline_summary", "quality_gate_ready"),
            ("listing_result", "publish_ready"),
            ("pipeline_summary", "publish_ready"),
        )
    )

    publish_ready = approval_status == "publish_ready"

    return {
        "file_name": path.name,
        "query": str(query),
        "status": status,
        "approval_status": approval_status,
        "quality_gate_ready": quality_gate_ready,
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

        rows.append((_record_sort_key(record, path), _read_run_row(path, record)))

    rows.sort(key=lambda item: item[0], reverse=True)
    return [item[1] for item in rows]


def _apply_filter(rows, status_filter):
    if status_filter is None:
        return rows

    if status_filter == "publish_ready":
        return [row for row in rows if row["publish_ready"]]

    return [row for row in rows if row["approval_status"] == status_filter]


def _truncate(text, width):
    if len(text) <= width:
        return text
    return text[: max(1, width - 3)] + "..."


def _format_bool(value):
    return "Y" if value else "N"


def _print_rows(rows):
    if not rows:
        print("No queue items found.")
        return

    print("file | query | status | approval | qgate | publish")
    print("-" * 80)

    for row in rows[:DEFAULT_LIMIT]:
        print(
            " | ".join(
                [
                    _truncate(row["file_name"], 26),
                    _truncate(row["query"].replace("\n", " "), 30),
                    _truncate(row["status"], 10),
                    _truncate(row["approval_status"], 12),
                    _format_bool(row["quality_gate_ready"]),
                    _format_bool(row["publish_ready"]),
                ]
            )
        )

    if len(rows) > DEFAULT_LIMIT:
        print(f"... showing latest {DEFAULT_LIMIT} of {len(rows)} runs")


def main():
    status_filter = None
    if len(sys.argv) > 2:
        print("Usage: python list_queue.py [review|approved|publish_ready]")
        return 1

    if len(sys.argv) == 2:
        status_filter = sys.argv[1].strip().lower()
        if status_filter not in SUPPORTED_FILTERS:
            print(f"Unsupported filter: {status_filter}")
            print("Supported filters: review, approved, publish_ready")
            return 1

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        print("No history found. The 'history/' folder does not exist yet.")
        return 0

    rows = _load_rows(HISTORY_DIR)
    if not rows:
        print("No history records found in 'history/'")
        return 0

    filtered = _apply_filter(rows, status_filter)
    _print_rows(filtered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
