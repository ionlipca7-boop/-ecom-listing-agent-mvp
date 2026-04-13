import json
import sys
from datetime import datetime
from pathlib import Path


HISTORY_DIR = Path("history")


def _extract_timestamp(record, path):
    timestamp = record.get("timestamp") if isinstance(record, dict) else None
    if isinstance(timestamp, str) and timestamp:
        return timestamp
    return path.stem


def _sort_key(path):
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


def _latest_history_file(history_dir):
    files = [path for path in history_dir.glob("run_*.json") if path.is_file()]
    if not files:
        return None
    files.sort(key=_sort_key, reverse=True)
    return files[0]


def _load_record(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _print_section(name, value):
    print(f"{name}:")
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _print_ai_fields(listing_result):
    print("AI fields inside listing_result:")
    if not isinstance(listing_result, dict):
        print("  - listing_result is not a JSON object")
        return

    ai_items = []
    for key, value in listing_result.items():
        if "ai" in key.lower():
            ai_items.append((key, value))

    final_bundle = listing_result.get("final_listing_bundle")
    if isinstance(final_bundle, dict):
        for key, value in final_bundle.items():
            if "ai" in key.lower():
                ai_items.append((f"final_listing_bundle.{key}", value))

    if not ai_items:
        print("  - no AI fields found")
        return

    for key, value in ai_items:
        print(f"  - {key}: {json.dumps(value, ensure_ascii=False)}")


def main():
    if len(sys.argv) > 2:
        print("Usage: python inspect_run.py [history/run_*.json]")
        return

    if len(sys.argv) == 2:
        run_path = Path(sys.argv[1])
        if not run_path.exists() or not run_path.is_file():
            print(f"Run record not found: {run_path}")
            return
    else:
        if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
            print("No history found. The 'history/' folder does not exist yet.")
            return

        run_path = _latest_history_file(HISTORY_DIR)
        if run_path is None:
            print("No history records found in 'history/'.")
            return

    record = _load_record(run_path)

    print(f"run_file: {run_path}")
    print(f"timestamp: {_extract_timestamp(record, run_path)}")
    _print_section("raw_input", record.get("raw_input"))
    _print_section("parsed_product", record.get("parsed_product"))
    _print_section("listing_result", record.get("listing_result"))
    _print_section("publish_result", record.get("publish_result"))
    _print_section("pipeline_summary", record.get("pipeline_summary"))
    _print_ai_fields(record.get("listing_result"))


if __name__ == "__main__":
    main()
