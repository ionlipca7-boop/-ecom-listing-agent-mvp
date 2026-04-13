import json
import sys
from datetime import datetime
from pathlib import Path


HISTORY_DIR = Path("history")
SUPPORTED_ACTIONS = {"approve", "publish_ready"}
CONTROL_STATUSES = {"review", "approved", "publish_ready"}
LEGACY_REVIEW_STATUSES = {"draft"}


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


def _save_record(path, record):
    with path.open("w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


def _read_old_status(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else {}
    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else {}

    if isinstance(listing_result, dict):
        for key in ("approval_status", "control_status", "status"):
            value = listing_result.get(key)
            if isinstance(value, str) and value:
                return value, key

    if isinstance(pipeline_summary, dict):
        for key in ("approval_status", "control_status", "status"):
            value = pipeline_summary.get(key)
            if isinstance(value, str) and value:
                return value, f"pipeline_summary.{key}"

    return "review", "default"


def _read_quality_gate_ready(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else {}
    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else {}

    candidates = []
    if isinstance(listing_result, dict):
        candidates.extend([
            listing_result.get("quality_gate_ready"),
            listing_result.get("publish_ready"),
        ])

    if isinstance(pipeline_summary, dict):
        candidates.extend([
            pipeline_summary.get("quality_gate_ready"),
            pipeline_summary.get("publish_ready"),
        ])

    for candidate in candidates:
        if candidate is not None:
            return _to_bool(candidate)

    return False


def _set_status(record, new_status):
    listing_result = record.get("listing_result") if isinstance(record, dict) else None
    if not isinstance(listing_result, dict):
        return

    is_publish_ready = new_status == "publish_ready"

    listing_result["approval_status"] = new_status
    listing_result["publish_ready"] = is_publish_ready

    current_status = listing_result.get("status")
    if isinstance(current_status, str) and current_status in CONTROL_STATUSES:
        listing_result["status"] = new_status

    final_bundle = listing_result.get("final_listing_bundle")
    if isinstance(final_bundle, dict):
        final_bundle["approval_status"] = new_status
        final_bundle["publish_ready"] = is_publish_ready
        bundle_status = final_bundle.get("status")
        if isinstance(bundle_status, str) and bundle_status in CONTROL_STATUSES:
            final_bundle["status"] = new_status

    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else None
    if isinstance(pipeline_summary, dict):
        pipeline_summary["approval_status"] = new_status
        pipeline_summary["publish_ready"] = is_publish_ready


def _apply_action(old_status, action, quality_gate_ready):
    normalized_old_status = old_status.strip().lower()
    effective_status = "review" if normalized_old_status in LEGACY_REVIEW_STATUSES else normalized_old_status

    if action == "approve":
        if effective_status == "review":
            if normalized_old_status in LEGACY_REVIEW_STATUSES:
                return True, "approved", "Transition applied: legacy draft treated as review -> approved"
            return True, "approved", "Transition applied: review -> approved"
        return False, old_status, "approve action is only allowed when status is review"

    if action == "publish_ready":
        if effective_status == "publish_ready":
            return True, "publish_ready", "No change: already publish_ready"
        if effective_status == "approved":
            return True, "publish_ready", "Transition applied: approved -> publish_ready"
        if effective_status == "review" and quality_gate_ready:
            if normalized_old_status in LEGACY_REVIEW_STATUSES:
                return True, "publish_ready", "Direct transition applied: legacy draft treated as review -> publish_ready (quality gate passed)"
            return True, "publish_ready", "Direct transition applied: review -> publish_ready (quality gate passed)"
        if effective_status == "review" and not quality_gate_ready:
            return False, old_status, "Direct publish_ready from review requires quality_gate_ready == True"
        return False, old_status, "publish_ready action requires status approved, or review with quality_gate_ready == True"

    return False, old_status, f"Unsupported action: {action}"


def main():
    if len(sys.argv) != 2:
        print("Usage: python approval_action.py <approve|publish_ready>")
        return 1

    action = sys.argv[1].strip().lower()
    if action not in SUPPORTED_ACTIONS:
        print(f"Unsupported action: {action}")
        print("Supported actions: approve, publish_ready")
        return 1

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        print("old status: -")
        print("new status: -")
        print("quality_gate_ready: False")
        print("result: fail")
        print("reason: No history found. The 'history/' folder does not exist yet.")
        return 1

    run_path = _latest_history_file(HISTORY_DIR)
    if run_path is None:
        print("old status: -")
        print("new status: -")
        print("quality_gate_ready: False")
        print("result: fail")
        print("reason: No history records found in 'history/'.")
        return 1

    record = _load_record(run_path)
    old_status, _ = _read_old_status(record)
    quality_gate_ready = _read_quality_gate_ready(record)

    success, new_status, reason = _apply_action(old_status, action, quality_gate_ready)

    if success:
        _set_status(record, new_status)
        _save_record(run_path, record)
        result_label = "success"
        exit_code = 0
    else:
        result_label = "fail"
        exit_code = 1

    print(f"old status: {old_status}")
    print(f"new status: {new_status}")
    print(f"quality_gate_ready: {quality_gate_ready}")
    print(f"result: {result_label}")
    print(f"reason: {reason}")
    print(f"run_file: {run_path}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
