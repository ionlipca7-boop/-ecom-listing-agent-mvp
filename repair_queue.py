import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


HISTORY_DIR = Path("history")
SUPPORTED_MODES = {"scan_legacy", "repair_approved_qgate"}
QUALITY_THRESHOLD = 90


def _to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    if isinstance(value, (int, float)):
        return value != 0
    return False


def _to_float(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


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


def _ensure_dict(parent, key):
    value = parent.get(key)
    if isinstance(value, dict):
        return value
    value = {}
    parent[key] = value
    return value


def _read_approval_status(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else None
    if isinstance(listing_result, dict):
        for key in ("approval_status", "control_status", "status"):
            value = listing_result.get(key)
            if isinstance(value, str) and value.strip():
                status = value.strip().lower()
                return "review" if status == "draft" else status

    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else None
    if isinstance(pipeline_summary, dict):
        for key in ("approval_status", "control_status", "status"):
            value = pipeline_summary.get(key)
            if isinstance(value, str) and value.strip():
                status = value.strip().lower()
                return "review" if status == "draft" else status

    return "review"


def _read_publish_ready(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else None
    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else None

    candidates = []
    if isinstance(listing_result, dict):
        candidates.append(listing_result.get("publish_ready"))
    if isinstance(pipeline_summary, dict):
        candidates.append(pipeline_summary.get("publish_ready"))

    for candidate in candidates:
        if candidate is not None:
            return _to_bool(candidate)

    return _read_approval_status(record) == "publish_ready"


def _read_quality_gate_ready(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else None
    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else None

    quality_values = []
    has_explicit_quality = False

    if isinstance(listing_result, dict) and "quality_gate_ready" in listing_result:
        has_explicit_quality = True
        quality_values.append(listing_result.get("quality_gate_ready"))

    final_bundle = listing_result.get("final_listing_bundle") if isinstance(listing_result, dict) else None
    if isinstance(final_bundle, dict) and "quality_gate_ready" in final_bundle:
        has_explicit_quality = True
        quality_values.append(final_bundle.get("quality_gate_ready"))

    if isinstance(pipeline_summary, dict) and "quality_gate_ready" in pipeline_summary:
        has_explicit_quality = True
        quality_values.append(pipeline_summary.get("quality_gate_ready"))

    for value in quality_values:
        if _to_bool(value):
            return True, has_explicit_quality

    if quality_values:
        return False, has_explicit_quality

    return False, has_explicit_quality


def _read_quality_score(record):
    listing_result = record.get("listing_result") if isinstance(record, dict) else None
    pipeline_summary = record.get("pipeline_summary") if isinstance(record, dict) else None

    candidates = []
    if isinstance(listing_result, dict):
        candidates.append(listing_result.get("listing_quality_score"))
    if isinstance(pipeline_summary, dict):
        candidates.append(pipeline_summary.get("quality_score"))

    for candidate in candidates:
        score = _to_float(candidate)
        if score is not None:
            return score

    return None


def _is_legacy_candidate(record):
    approval_status = _read_approval_status(record)
    if approval_status != "approved":
        return False, "status_not_approved"

    if _read_publish_ready(record):
        return False, "already_publish_ready"

    quality_gate_ready, _ = _read_quality_gate_ready(record)
    if quality_gate_ready:
        return False, "quality_gate_already_true"

    return True, "candidate"


def _score_allows_repair(record):
    score = _read_quality_score(record)
    if score is None:
        return False, "score_missing"
    if score < QUALITY_THRESHOLD:
        return False, "score_below_threshold"
    return True, "score_ok"


def _repair_record(record):
    if not isinstance(record, dict):
        return False

    listing_result = _ensure_dict(record, "listing_result")
    final_bundle = _ensure_dict(listing_result, "final_listing_bundle")
    pipeline_summary = _ensure_dict(record, "pipeline_summary")

    listing_result["quality_gate_ready"] = True
    final_bundle["quality_gate_ready"] = True
    pipeline_summary["quality_gate_ready"] = True

    return True


def _print_summary(scanned, repaired, skipped, reasons):
    print(f"scanned: {scanned}")
    print(f"repaired: {repaired}")
    print(f"skipped: {skipped}")
    if not reasons:
        print("reasons_summary: -")
        return

    joined = ", ".join(f"{name}={count}" for name, count in sorted(reasons.items()))
    print(f"reasons_summary: {joined}")


def main():
    mode = "scan_legacy"

    if len(sys.argv) > 2:
        print("Usage: python repair_queue.py [scan_legacy|repair_approved_qgate]")
        return 1

    if len(sys.argv) == 2:
        mode = sys.argv[1].strip().lower()

    if mode not in SUPPORTED_MODES:
        print(f"Unsupported mode: {mode}")
        print("Supported modes: scan_legacy, repair_approved_qgate")
        return 1

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        print("No history found. The 'history/' folder does not exist yet.")
        _print_summary(0, 0, 0, Counter())
        return 0

    files = _history_files(HISTORY_DIR)
    if not files:
        print("No history records found in 'history/'")
        _print_summary(0, 0, 0, Counter())
        return 0

    scanned = 0
    repaired = 0
    reasons = Counter()

    for path in files:
        scanned += 1
        try:
            record = _load_record(path)
        except (OSError, json.JSONDecodeError):
            reasons["invalid_json_or_io"] += 1
            continue

        is_candidate, reject_reason = _is_legacy_candidate(record)
        if not is_candidate:
            reasons[reject_reason] += 1
            continue

        score_ok, score_reason = _score_allows_repair(record)
        if not score_ok:
            reasons[score_reason] += 1
            continue

        if mode == "repair_approved_qgate":
            if _repair_record(record):
                _save_record(path, record)
                repaired += 1
            else:
                reasons["record_not_dict"] += 1
                continue
        else:
            reasons["scan_only_candidate"] += 1

    skipped = scanned - repaired
    _print_summary(scanned, repaired, skipped, reasons)

    if mode == "scan_legacy":
        print("mode: scan only (no files changed)")
    else:
        print("mode: repair applied to eligible records")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
