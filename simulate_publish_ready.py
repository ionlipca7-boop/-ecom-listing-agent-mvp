import json
from datetime import UTC, datetime
from pathlib import Path

from list_queue import HISTORY_DIR, _apply_filter, _load_rows


PUBLISH_LOGS_DIR = Path("publish_logs")


def _build_output_path() -> Path:
    PUBLISH_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    return PUBLISH_LOGS_DIR / f"simulate_publish_ready_{timestamp}.json"


def _build_simulated_items(rows: list[dict]) -> list[dict]:
    simulated_at = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
    simulated_items = []

    for row in rows:
        simulated_items.append(
            {
                "file_name": row["file_name"],
                "query": row["query"],
                "status": row["status"],
                "approval_status": row["approval_status"],
                "quality_gate_ready": row["quality_gate_ready"],
                "publish_ready": row["publish_ready"],
                "simulation_status": "simulated",
                "simulated_at": simulated_at,
            }
        )

    return simulated_items


def main() -> int:
    output_path = _build_output_path()

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        payload = {
            "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "scanned": 0,
            "simulated": 0,
            "items": [],
        }
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("scanned: 0")
        print("simulated: 0")
        print(f"output_file: {output_path}")
        return 0

    queue_rows = _load_rows(HISTORY_DIR)
    publish_ready_rows = _apply_filter(queue_rows, "publish_ready")
    simulated_items = _build_simulated_items(publish_ready_rows)

    payload = {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "scanned": len(queue_rows),
        "simulated": len(simulated_items),
        "items": simulated_items,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"scanned: {len(queue_rows)}")
    print(f"simulated: {len(simulated_items)}")
    print(f"output_file: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
