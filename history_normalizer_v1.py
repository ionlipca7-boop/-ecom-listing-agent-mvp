import argparse
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

SOURCE_HISTORY_DIR = Path("control_room_history")
INDEX_PATH = Path("control_room_history_index.json")
BACKUP_PATH = Path("control_room_history_index.backup_v1.json")

SCHEMA_KEYS = ("timestamp", "status", "package", "next_step", "reason", "file")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize control room history index.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files")
    return parser.parse_args()


def _safe_json_load(path: Path) -> Any | None:
    if not path.exists() or not path.is_file() or path.stat().st_size == 0:
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _as_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _resolve_file_path(file_value: str | None) -> Path | None:
    if not file_value:
        return None

    raw = Path(file_value)
    if raw.exists() and raw.is_file():
        return raw

    alt = SOURCE_HISTORY_DIR / Path(file_value).name
    if alt.exists() and alt.is_file():
        return alt

    return None


def _extract_from_payload(payload: dict[str, Any]) -> dict[str, str | None]:
    return {
        "timestamp": _as_text(payload.get("timestamp") or payload.get("checked_at")),
        "status": _as_text(payload.get("status") or payload.get("dashboard_status")),
        "package": _as_text(payload.get("package") or payload.get("last_package")),
        "next_step": _as_text(payload.get("next_step")),
        "reason": _as_text(payload.get("reason")),
    }


def _entry_from_file(file_path: Path) -> dict[str, Any]:
    payload = _safe_json_load(file_path)
    if not isinstance(payload, dict):
        return {"file": str(file_path)}

    extracted = _extract_from_payload(payload)
    extracted["file"] = str(file_path)
    return extracted


def _normalize_entry(raw: dict[str, Any]) -> dict[str, str | None] | None:
    normalized: dict[str, str | None] = {
        "timestamp": _as_text(raw.get("timestamp") or raw.get("checked_at")),
        "status": _as_text(raw.get("status") or raw.get("dashboard_status")),
        "package": _as_text(raw.get("package") or raw.get("last_package")),
        "next_step": _as_text(raw.get("next_step")),
        "reason": _as_text(raw.get("reason")),
        "file": _as_text(raw.get("file")),
    }

    file_path = _resolve_file_path(normalized["file"])
    if file_path is not None:
        payload = _safe_json_load(file_path)
        if isinstance(payload, dict):
            extracted = _extract_from_payload(payload)
            for key in ("timestamp", "status", "package", "next_step", "reason"):
                if not normalized[key]:
                    normalized[key] = extracted[key]
        normalized["file"] = str(file_path)

    if not normalized["timestamp"] or not normalized["status"]:
        return None

    return normalized


def _dedup_key(entry: dict[str, str | None]) -> tuple[Any, ...]:
    return (
        entry.get("timestamp"),
        entry.get("status"),
        entry.get("package"),
        entry.get("next_step"),
        entry.get("reason"),
        entry.get("file"),
    )


def _sort_key(entry: dict[str, str | None]) -> tuple[str, str]:
    return (
        str(entry.get("timestamp") or ""),
        str(entry.get("file") or ""),
    )


def _load_existing_index() -> list[dict[str, Any]]:
    data = _safe_json_load(INDEX_PATH)
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        runs = data.get("runs")
        if isinstance(runs, list):
            return [row for row in runs if isinstance(row, dict)]
    return []


def _load_source_file_entries() -> list[dict[str, Any]]:
    if not SOURCE_HISTORY_DIR.exists() or not SOURCE_HISTORY_DIR.is_dir():
        return []

    entries: list[dict[str, Any]] = []
    for path in sorted(SOURCE_HISTORY_DIR.glob("run_*.json")):
        if path.is_file():
            entries.append(_entry_from_file(path))
    return entries


def _build_normalized_entries() -> tuple[list[dict[str, str | None]], dict[str, int]]:
    existing = _load_existing_index()
    from_files = _load_source_file_entries()
    candidates = existing + from_files

    stats = {
        "existing_index_entries": len(existing),
        "source_file_entries": len(from_files),
        "candidates": len(candidates),
        "kept": 0,
        "invalid": 0,
        "duplicates": 0,
    }

    dedup_map: dict[tuple[Any, ...], dict[str, str | None]] = {}

    for raw in candidates:
        normalized = _normalize_entry(raw)
        if normalized is None:
            stats["invalid"] += 1
            continue

        key = _dedup_key(normalized)
        if key in dedup_map:
            stats["duplicates"] += 1
        dedup_map[key] = normalized

    entries = sorted(dedup_map.values(), key=_sort_key)
    stats["kept"] = len(entries)
    return entries, stats


def _atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=str(path.parent), delete=False) as tmp:
        json.dump(payload, tmp, ensure_ascii=False, indent=2)
        tmp.write("\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def _write_backup_before_index_write() -> None:
    if not INDEX_PATH.exists() or not INDEX_PATH.is_file():
        return

    current_data = _safe_json_load(INDEX_PATH)
    if current_data is None:
        current_data = []
    _atomic_write_json(BACKUP_PATH, current_data)


def main() -> int:
    args = _parse_args()
    entries, stats = _build_normalized_entries()

    print(f"source_history_dir={SOURCE_HISTORY_DIR}")
    print(f"index_path={INDEX_PATH}")
    print(f"backup_path={BACKUP_PATH}")
    for key, value in stats.items():
        print(f"{key}={value}")

    if args.dry_run:
        print("dry_run=true (no files written)")
        return 0

    _write_backup_before_index_write()
    _atomic_write_json(INDEX_PATH, entries)
    print("dry_run=false (backup + index write complete)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())