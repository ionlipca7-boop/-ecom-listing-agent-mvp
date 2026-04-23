import json
import urllib.parse
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
EXPORTS_DIR = STORAGE_DIR / "exports"
REGISTRY_DIR = STORAGE_DIR / "registry"
SECRETS_DIR = STORAGE_DIR / "secrets"

REGISTRY_PATH = REGISTRY_DIR / "live_listings_registry_v1.json"
ACTION_PATH = EXPORTS_DIR / "control_action_get_live_status_v1.json"
PRECHECK_PATH = EXPORTS_DIR / "control_action_get_live_status_precheck_v3.json"
AUDIT_PATH = EXPORTS_DIR / "control_action_get_live_status_audit_v3.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"

DEFAULT_PRODUCT_KEY = "cable_001"

def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def read_token(path):
    token = path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
    if not token:
        raise ValueError("Access token file is empty")
    return token

def resolve_action():
    action = load_json(ACTION_PATH, {})
    product_key = action.get("product_key") or DEFAULT_PRODUCT_KEY
    return {"product_key": product_key}

def resolve_registry_entry(product_key):
    registry = load_json(REGISTRY_PATH, {"items": []})
    items = registry.get("items", []) if isinstance(registry, dict) else []
    for item in items:
        if isinstance(item, dict) and item.get("product_key") == product_key:
            return item
    return None

def main():
    action = resolve_action()
    entry = resolve_registry_entry(action["product_key"])

    precheck = {
        "status": "OK" if entry else "ERROR",
        "decision": "control_action_get_live_status_precheck_completed" if entry else "registry_entry_not_found",
        "product_key": action["product_key"],
        "registry_entry_found": bool(entry),
        "sku": entry.get("sku") if entry else None,
        "offerId": entry.get("offerId") if entry else None,
        "listingId": entry.get("listingId") if entry else None,
        "listing_state": entry.get("listing_state") if entry else None
    }
    write_json(PRECHECK_PATH, precheck)

    if not entry:
        print("CONTROL_ACTION_GET_LIVE_STATUS_FAILED")
        print("decision = registry_entry_not_found")
        print("product_key =", action["product_key"])
        return

    token = read_token(TOKEN_PATH)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }

    sku = str(entry.get("sku")).strip()
    sku_encoded = urllib.parse.quote(sku, safe="")
    inventory_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku_encoded}"
    inventory_response = requests.get(inventory_url, headers=headers, timeout=60)

    audit = {
        "status": "UNKNOWN",
        "decision": "control_action_get_live_status_started",
        "product_key": action["product_key"],
        "sku": sku,
        "offerId": entry.get("offerId"),
        "listingId": entry.get("listingId"),
        "registry_listing_state": entry.get("listing_state"),
        "registry_pipeline_status": entry.get("pipeline_status"),
        "inventory_http_status": inventory_response.status_code,
        "live_quantity": None,
        "image_count": None,
        "has_produktart": False,
        "response_text": inventory_response.text[:4000]
    }

    if inventory_response.status_code != 200:
        audit["status"] = "ERROR"
        audit["decision"] = "inventory_status_read_failed"
        write_json(AUDIT_PATH, audit)
        print("CONTROL_ACTION_GET_LIVE_STATUS_FAILED")
        print("decision = inventory_status_read_failed")
        print("product_key =", action["product_key"])
        print("sku =", sku)
        print("inventory_http_status =", inventory_response.status_code)
        return

    item = inventory_response.json()
    availability = item.get("availability", {}) if isinstance(item, dict) else {}
    ship = availability.get("shipToLocationAvailability", {}) if isinstance(availability, dict) else {}
    product = item.get("product", {}) if isinstance(item, dict) else {}
    aspects = product.get("aspects", {}) if isinstance(product, dict) else {}
    image_urls = product.get("imageUrls", []) if isinstance(product, dict) else []
    produktart = aspects.get("Produktart") if isinstance(aspects, dict) else None

    audit["live_quantity"] = ship.get("quantity") if isinstance(ship, dict) else None
    audit["has_produktart"] = bool(produktart)
    audit["inventory_snapshot"] = item
    audit["status"] = "OK"
    audit["decision"] = "live_status_loaded_via_registry"
    write_json(AUDIT_PATH, audit)

    print("CONTROL_ACTION_GET_LIVE_STATUS_OK")
    print("decision = live_status_loaded_via_registry")
    print("product_key =", action["product_key"])
    print("sku =", sku)
    print("live_quantity =", audit["live_quantity"])
    print("image_count =", audit["image_count"])
    print("has_produktart =", audit["has_produktart"])

if __name__ == "__main__":
    main()
