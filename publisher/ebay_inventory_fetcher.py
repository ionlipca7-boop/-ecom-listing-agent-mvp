import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ENV_PATH = Path(".env.local")
SNAPSHOT_PATH = Path("storage/inventory/ebay_active_listings_snapshot_v1.json")
API_URL = "https://api.ebay.com/sell/inventory/v1/inventory_item?limit=200"


def load_env(path=ENV_PATH):
    data = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                data[k.strip()] = v.strip()
    return data


def get_access_token():
    return load_env().get("EBAY_ACCESS_TOKEN", "")


def normalize_inventory_item(raw):
    raw = raw or {}
    product = raw.get("product", {}) or {}
    availability = raw.get("availability", {}) or {}
    ship_to = availability.get("shipToLocationAvailability", {}) or {}
    return {"item_id": raw.get("sku"), "title": product.get("title"), "price": None, "currency": "EUR", "quantity": ship_to.get("quantity"), "status": "active_or_inventory", "url": None, "image_urls": product.get("imageUrls", []) or [], "views": None, "watchers": None, "last_updated": None, "raw": raw}


def fetch_inventory_items():
    token = get_access_token()
    if not token:
        return {"ok": False, "api_call_used": False, "error": "missing_access_token", "items": []}
    req = urllib.request.Request(API_URL, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json", "Accept": "application/json"}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    raw_items = payload.get("inventoryItems", [])
    items = [normalize_inventory_item(i) for i in raw_items]
    return {"ok": True, "api_call_used": True, "count": len(items), "items": items, "raw": payload}


def save_snapshot(items, path=SNAPSHOT_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"status": "OK", "mode": "REAL_EBAY_READ_ONLY_INVENTORY", "count": len(items), "items": items, "created_at": datetime.now(timezone.utc).isoformat()}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
