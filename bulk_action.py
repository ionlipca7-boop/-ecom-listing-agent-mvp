import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


HISTORY_DIR = Path("history")
SUPPORTED_ACTIONS = {"approve_all_review", "publish_ready_all_approved"}


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


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


def _history_files(history_dir):
    files = [path for path in history_dir.glob("run_*.json") if path.is_file()]
    files.sort(key=_sort_key, reverse=True)
    return files


def _load_record(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_record(path, record):
    with path.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def _read_status(record):
    if not isinstance(record, dict):
        return "review"

    listing_result = record.get("listing_result")
    pipeline_summary = record.get("pipeline_summary")

    if isinstance(listing_result, dict):
        for key in ("approval_status", "control_status", "status"):
            value = listing_result.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip().lower()

    if isinstance(pipeline_summary, dict):
        for key in ("approval_status", "control_status", "status"):
            value = pipeline_summary.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip().lower()

    return "review"


def _read_quality_gate_ready(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else {}
    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else {}

    candidates = []
    if isinstance(listing_result, dict):
        candidates.extend(
            [
                listing_result.get("quality_gate_ready"),
                listing_result.get("publish_ready"),
            ]
        )

    if isinstance(pipeline_summary, dict):
        candidates.extend(
            [
                pipeline_summary.get("quality_gate_ready"),
                pipeline_summary.get("publish_ready"),
            ]
        )

    for candidate in candidates:
        if candidate is not None:
            return _to_bool(candidate)

    return False


def _set_status(record, new_status):
    if not isinstance(record, dict):
        return

    listing_result = record.get("listing_result")
    if isinstance(listing_result, dict):
        listing_result["approval_status"] = new_status
        if isinstance(listing_result.get("status"), str):
            listing_result["status"] = new_status
        listing_result["publish_ready"] = new_status == "publish_ready"

        final_bundle = listing_result.get("final_listing_bundle")
        if isinstance(final_bundle, dict):
            final_bundle["approval_status"] = new_status
            if isinstance(final_bundle.get("status"), str):
                final_bundle["status"] = new_status
            final_bundle["publish_ready"] = new_status == "publish_ready"

    pipeline_summary = record.get("pipeline_summary")
    if isinstance(pipeline_summary, dict):
        pipeline_summary["approval_status"] = new_status
        if isinstance(pipeline_summary.get("status"), str):
            pipeline_summary["status"] = new_status
        pipeline_summary["publish_ready"] = new_status == "publish_ready"


def _apply_rule(action, status, quality_gate_ready):
    normalized = "review" if status == "draft" else status

    if action == "approve_all_review":
        if normalized == "review":
            return True, "approved", None
        return False, status, f"status_not_review:{normalized}"

    if action == "publish_ready_all_approved":
        if normalized != "approved":
            return False, status, f"status_not_approved:{normalized}"
        if not quality_gate_ready:
            return False, status, "quality_gate_not_ready"
        return True, "publish_ready", None

    return False, status, "unsupported_action"


def _print_summary(scanned, changed, skipped, reasons):
    print(f"scanned: {scanned}")
    print(f"changed: {changed}")
    print(f"skipped: {skipped}")

    if not reasons:
        print("reasons_summary: -")
        return

    formatted = ", ".join(f"{reason}={count}" for reason, count in sorted(reasons.items()))
    print(f"reasons_summary: {formatted}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python bulk_action.py <approve_all_review|publish_ready_all_approved>")
        return 1

    action = sys.argv[1].strip().lower()
    if action not in SUPPORTED_ACTIONS:
        print(f"Unsupported action: {action}")
        print("Supported actions: approve_all_review, publish_ready_all_approved")
        return 1

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        print("No history found. The 'history/' folder does not exist yet.")
        return 0

    files = _history_files(HISTORY_DIR)
    if not files:
        print("No history records found in 'history/'")
        return 0

    scanned = 0
    changed = 0
    reasons = Counter()

    for path in files:
        scanned += 1
        try:
            record = _load_record(path)
        except (OSError, json.JSONDecodeError):
            reasons["invalid_json_or_io"] += 1
            continue

        status = _read_status(record)
        quality_gate_ready = _read_quality_gate_ready(record)

        should_change, new_status, reason = _apply_rule(action, status, quality_gate_ready)
        if not should_change:
            reasons[reason] += 1
            continue

        _set_status(record, new_status)
        _save_record(path, record)
        changed += 1

    skipped = scanned - changed
    _print_summary(scanned, changed, skipped, reasons)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
