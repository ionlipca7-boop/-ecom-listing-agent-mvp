import json
import sys
from datetime import datetime
from pathlib import Path


HISTORY_DIR = Path("history")
EXPORTS_DIR = Path("exports")
AI_FIELDS = [
    "search_intents",
    "compatibility_keywords",
    "use_case_keywords",
    "seo_keywords",
    "buyer_questions",
    "ai_summary",
]


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


def _extract_timestamp(record, run_path):
    timestamp = record.get("timestamp") if isinstance(record, dict) else None
    if isinstance(timestamp, str) and timestamp:
        return timestamp
    return run_path.stem.replace("run_", "")


def _normalize_run_path(user_input):
    return Path(str(user_input).replace("\\", "/"))


def _load_record(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _json_block(value):
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2) + "\n```\n"


def _collect_ai_fields(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else {}
    final_bundle = listing_result.get("final_listing_bundle") if isinstance(listing_result, dict) else {}

    ai_data = {}
    for field in AI_FIELDS:
        if isinstance(final_bundle, dict) and field in final_bundle:
            ai_data[field] = final_bundle.get(field)
        elif isinstance(listing_result, dict) and field in listing_result:
            ai_data[field] = listing_result.get(field)
        else:
            ai_data[field] = None
    return ai_data


def _build_report(run_path, record):
    timestamp = _extract_timestamp(record, run_path)
    ai_fields = _collect_ai_fields(record)

    lines = [
        "# Run Export Report",
        "",
        "## Run file",
        f"`{run_path}`",
        "",
        "## Timestamp",
        f"`{timestamp}`",
        "",
        "## Raw input",
        _json_block(record.get("raw_input")),
        "## Parsed product",
        _json_block(record.get("parsed_product")),
        "## Listing result",
        _json_block(record.get("listing_result")),
        "## Publish result",
        _json_block(record.get("publish_result")),
        "## Pipeline summary",
        _json_block(record.get("pipeline_summary")),
        "## AI-ready fields",
        _json_block(ai_fields),
    ]
    return "\n".join(lines)


def _export_path_for(run_path):
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return EXPORTS_DIR / f"{run_path.stem}.md"


def main():
    if len(sys.argv) > 2:
        print("Usage: python export_run.py [history/run_*.json]")
        return

    if len(sys.argv) == 2:
        run_path = _normalize_run_path(sys.argv[1])
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
    report_text = _build_report(run_path, record)
    export_path = _export_path_for(run_path)

    with export_path.open("w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Export created: {export_path}")


if __name__ == "__main__":
    main()
