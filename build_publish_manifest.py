import json
from datetime import UTC, datetime
from pathlib import Path

from list_queue import HISTORY_DIR, _apply_filter, _load_rows


PUBLISH_MANIFESTS_DIR = Path("publish_manifests")


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _build_output_path() -> tuple[str, Path]:
    PUBLISH_MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    manifest_id = f"publish_manifest_{timestamp}"
    return manifest_id, PUBLISH_MANIFESTS_DIR / f"{manifest_id}.json"


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


def _manifest_item_from_row(row: dict) -> dict:
    record = _load_run_record(row["file_name"])
    listing_result = record.get("listing_result") if isinstance(record.get("listing_result"), dict) else {}
    final_listing_bundle = (
        listing_result.get("final_listing_bundle")
        if isinstance(listing_result.get("final_listing_bundle"), dict)
        else {}
    )

    title = final_listing_bundle.get("title", listing_result.get("title"))
    category = final_listing_bundle.get("category", listing_result.get("category"))
    price = final_listing_bundle.get("price", listing_result.get("price"))
    description = final_listing_bundle.get("description", listing_result.get("description"))
    item_specifics = final_listing_bundle.get("item_specifics", listing_result.get("item_specifics", {}))
    publish_status = final_listing_bundle.get("approval_status", listing_result.get("approval_status", row["approval_status"]))

    return {
        "source_run_file": row["file_name"],
        "title": title,
        "category": category,
        "price": price,
        "description": description,
        "item_specifics": item_specifics if isinstance(item_specifics, dict) else {},
        "publish_status": publish_status,
    }


def main() -> int:
    manifest_id, output_path = _build_output_path()

    if not HISTORY_DIR.exists() or not HISTORY_DIR.is_dir():
        payload = {
            "manifest_id": manifest_id,
            "generated_at": _utc_now_iso(),
            "total_items": 0,
            "items": [],
        }
        output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("scanned: 0")
        print("total_items: 0")
        print(f"output_file: {output_path}")
        return 0

    queue_rows = _load_rows(HISTORY_DIR)
    publish_ready_rows = _apply_filter(queue_rows, "publish_ready")
    manifest_items = [_manifest_item_from_row(row) for row in publish_ready_rows]

    payload = {
        "manifest_id": manifest_id,
        "generated_at": _utc_now_iso(),
        "total_items": len(manifest_items),
        "items": manifest_items,
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"scanned: {len(queue_rows)}")
    print(f"total_items: {len(manifest_items)}")
    print(f"output_file: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
