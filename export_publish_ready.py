import json
from datetime import UTC, datetime
from pathlib import Path

from list_queue import HISTORY_DIR, _apply_filter, _load_rows


EXPORTS_DIR = Path("exports")


def _build_output_path() -> Path:
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    return EXPORTS_DIR / f"publish_ready_{timestamp}.json"


def main() -> int:
    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        output_path = _build_output_path()
        payload = {
            "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "scanned": 0,
            "exported": 0,
            "items": [],
        }
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("scanned: 0")
        print("exported: 0")
        print(f"output_file: {output_path}")
        return 0

    queue_rows = _load_rows(HISTORY_DIR)
    publish_ready_rows = _apply_filter(queue_rows, "publish_ready")

    output_path = _build_output_path()
    payload = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "scanned": len(queue_rows),
        "exported": len(publish_ready_rows),
        "items": publish_ready_rows,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"scanned: {len(queue_rows)}")
    print(f"exported: {len(publish_ready_rows)}")
    print(f"output_file: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
