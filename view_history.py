import json
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_COUNT = 5


def _parse_count_arg(argv):
    if len(argv) < 2:
        return DEFAULT_COUNT

    try:
        count = int(argv[1])
    except ValueError:
        print(f"Invalid count '{argv[1]}'. Using default: {DEFAULT_COUNT}.")
        return DEFAULT_COUNT

    if count <= 0:
        print(f"Count must be positive. Using default: {DEFAULT_COUNT}.")
        return DEFAULT_COUNT

    return count


def _record_sort_key(record, path):
    timestamp = record.get("timestamp") if isinstance(record, dict) else None
    if isinstance(timestamp, str):
        try:
            return datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
        except ValueError:
            pass

    return datetime.fromtimestamp(path.stat().st_mtime)


def _load_history_records(history_dir):
    records = []
    for path in history_dir.glob("*.json"):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue

        records.append((path, data))

    records.sort(key=lambda item: _record_sort_key(item[1], item[0]), reverse=True)
    return records


def _pick_field(record, *paths):
    for path in paths:
        value = record
        ok = True
        for key in path:
            if not isinstance(value, dict) or key not in value:
                ok = False
                break
            value = value[key]
        if ok:
            return value
    return None


def main():
    count = _parse_count_arg(sys.argv)

    history_dir = Path("history")
    if not history_dir.exists() or not history_dir.is_dir():
        print("No history found. The 'history/' folder does not exist yet.")
        return

    records = _load_history_records(history_dir)
    if not records:
        print("No history records found in 'history/'.")
        return

    print(f"Recent pipeline runs (showing up to {count}):")
    for index, (path, record) in enumerate(records[:count], start=1):
        timestamp = _pick_field(record, ("timestamp",)) or path.stem
        raw_input = _pick_field(record, ("raw_input",)) or "-"
        title = _pick_field(record, ("listing_result", "title"), ("publish_result", "title"), ("title",)) or "-"
        category = _pick_field(record, ("listing_result", "category"), ("publish_result", "category"), ("category",)) or "-"
        price = _pick_field(record, ("listing_result", "price"), ("publish_result", "price"), ("price",))
        publish_status = _pick_field(record, ("pipeline_summary", "publish_status"), ("publish_result", "status"), ("publish_status",)) or "-"

        print(f"{index}. [{timestamp}] {raw_input}")
        print(f"   title: {title}")
        print(f"   category: {category}")
        print(f"   price: {price if price is not None else '-'}")
        print(f"   publish_status: {publish_status}")


if __name__ == "__main__":
    main()
