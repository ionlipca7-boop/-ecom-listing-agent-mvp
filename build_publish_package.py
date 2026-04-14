import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from build_publish_manifest import _manifest_item_from_row
from export_publish_ready_csv import CSV_COLUMNS, _row_to_csv_record
from list_queue import HISTORY_DIR, _apply_filter, _load_rows
from simulate_publish_ready import _build_simulated_items

PUBLISH_PACKAGES_DIR = Path("publish_packages")


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _build_package_dir() -> tuple[str, Path]:
    PUBLISH_PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    package_id = f"package_{timestamp}"
    package_dir = PUBLISH_PACKAGES_DIR / package_id
    package_dir.mkdir(parents=True, exist_ok=True)
    return package_id, package_dir


def _load_run_record(file_name: str) -> dict:
    path = HISTORY_DIR / file_name
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def _write_manifest(path: Path, package_id: str, rows: list[dict]) -> None:
    items = [_manifest_item_from_row(row) for row in rows]
    payload = {
        "manifest_id": package_id,
        "generated_at": _utc_now_iso(),
        "total_items": len(items),
        "items": items,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict]) -> None:
    csv_rows = []
    for row in rows:
        record = _load_run_record(row["file_name"])
        if not record:
            continue
        csv_rows.append(_row_to_csv_record(row["file_name"], record))

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(csv_rows)


def _write_simulation(path: Path, scanned: int, rows: list[dict]) -> None:
    items = _build_simulated_items(rows)
    payload = {
        "generated_at": _utc_now_iso(),
        "scanned": scanned,
        "simulated": len(items),
        "items": items,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_meta(path: Path, package_id: str, total_items: int) -> None:
    payload = {
        "package_id": package_id,
        "generated_at": _utc_now_iso(),
        "total_items": total_items,
        "source": "publish_ready_queue",
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    package_id, package_dir = _build_package_dir()

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        queue_rows = []
        publish_ready_rows = []
    else:
        queue_rows = _load_rows(HISTORY_DIR)
        publish_ready_rows = _apply_filter(queue_rows, "publish_ready")

    _write_manifest(package_dir / "manifest.json", package_id, publish_ready_rows)
    _write_csv(package_dir / "listings.csv", publish_ready_rows)
    _write_simulation(package_dir / "simulation.json", len(queue_rows), publish_ready_rows)
    _write_meta(package_dir / "meta.json", package_id, len(publish_ready_rows))

    print(f"scanned: {len(queue_rows)}")
    print(f"total_items: {len(publish_ready_rows)}")
    print(f"output_dir: {package_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
