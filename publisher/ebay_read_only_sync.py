import os
import json
from pathlib import Path
from datetime import datetime, timezone

SNAPSHOT_PATH = Path("storage/inventory/ebay_active_listings_snapshot_v1.json")
REQUIRED_ENV = ["EBAY_ACCESS_TOKEN", "EBAY_REFRESH_TOKEN", "EBAY_CLIENT_ID", "EBAY_CLIENT_SECRET"]


def verify_token_presence():
    return {"ok": True, "mode": "READ_ONLY_CHECK", "present": {k: bool(os.getenv(k)) for k in REQUIRED_ENV}, "api_call_used": False}


def normalize_listing(raw):
    raw = raw or {}
    return {"item_id": raw.get("item_id") or raw.get("ItemID"), "title": raw.get("title") or raw.get("Title"), "price": raw.get("price") or raw.get("Price"), "currency": raw.get("currency") or raw.get("Currency", "EUR"), "quantity": raw.get("quantity") or raw.get("Quantity"), "status": raw.get("status") or raw.get("Status", "active"), "url": raw.get("url") or raw.get("ViewItemURL"), "image_urls": raw.get("image_urls") or raw.get("PictureURL") or [], "views": raw.get("views"), "watchers": raw.get("watchers"), "last_updated": raw.get("last_updated"), "raw": raw}


def get_active_listings():
    return {"ok": False, "mode": "READ_ONLY_STUB", "api_call_used": False, "items": [], "message": "Real eBay API read not connected yet"}


def save_inventory_snapshot(items, path=SNAPSHOT_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"status": "OK", "mode": "READ_ONLY_SNAPSHOT", "count": len(items), "items": items, "created_at": datetime.now(timezone.utc).isoformat()}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
