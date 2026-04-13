import json
from datetime import datetime
from pathlib import Path


HISTORY_DIR = Path("history")
LATEST_LIMIT = 5


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


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


def _truncate(text, width):
    if len(text) <= width:
        return text
    return text[: max(1, width - 3)] + "..."


def _format_bool(value):
    return "Y" if value else "N"


def _compute_summary(rows):
    review_count = sum(1 for row in rows if row["approval_status"] == "review")
    approved_count = sum(1 for row in rows if row["approval_status"] == "approved")
    publish_ready_count = sum(1 for row in rows if row["publish_ready"])
    approved_with_qgate = sum(
        1
        for row in rows
        if row["approval_status"] == "approved" and row["quality_gate_ready"]
    )

    return {
        "total_runs": len(rows),
        "review_count": review_count,
        "approved_count": approved_count,
        "publish_ready_count": publish_ready_count,
        "approved_with_qgate": approved_with_qgate,
    }


def _print_latest_rows(rows):
    print("latest 5 runs")
    print("file | query | approval | qgate | publish")
    print("-" * 80)

    for row in rows[:LATEST_LIMIT]:
        print(
            " | ".join(
                [
                    _truncate(row["file_name"], 26),
                    _truncate(row["query"].replace("\n", " "), 32),
                    _truncate(row["approval_status"], 12),
                    _format_bool(row["quality_gate_ready"]),
                    _format_bool(row["publish_ready"]),
                ]
            )
        )

    if not rows:
        print("-")


def _build_operator_hint(summary):
    if summary["review_count"] > 0:
        return "Operator hint: Review queue detected — run approval step (e.g. approve_all_review.bat)."

    if summary["approved_with_qgate"] > 0:
        return "Operator hint: Approved + quality gate ready detected — move items to publish_ready."

    return "Operator hint: Queue is empty — run pipeline to generate new listings."


def main():
    print("=== ECOM Listing Agent: Control Room Status v1 ===")

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        print("history folder: missing")
        print("total runs: 0")
        print("review count: 0")
        print("approved count: 0")
        print("publish_ready count: 0")
        print()
        _print_latest_rows([])
        print()
        print("Operator hint: Queue is empty — run pipeline to generate new listings.")
        return 0

    rows = _load_rows(HISTORY_DIR)
    summary = _compute_summary(rows)

    print(f"history folder: {HISTORY_DIR}")
    print(f"total runs: {summary['total_runs']}")
    print(f"review count: {summary['review_count']}")
    print(f"approved count: {summary['approved_count']}")
    print(f"publish_ready count: {summary['publish_ready_count']}")
    print()

    _print_latest_rows(rows)
    print()
    print(_build_operator_hint(summary))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
