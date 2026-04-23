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
ACTION_PATH = EXPORTS_DIR / "control_action_update_live_quantity_v1.json"
PRECHECK_PATH = EXPORTS_DIR / "control_action_update_live_quantity_precheck_v1.json"
AUDIT_PATH = EXPORTS_DIR / "control_action_update_live_quantity_audit_v1.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"

DEFAULT_PRODUCT_KEY = "cable_001"
DEFAULT_NEW_QUANTITY = 12

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
    new_quantity = action.get("new_quantity", DEFAULT_NEW_QUANTITY)
    return {"product_key": product_key, "new_quantity": int(new_quantity)}

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
        "decision": "control_action_update_live_quantity_precheck_completed" if entry else "registry_entry_not_found",
        "product_key": action["product_key"],
        "requested_quantity": action["new_quantity"],
        "registry_entry_found": bool(entry),
        "sku": entry.get("sku") if entry else None,
        "listing_state": entry.get("listing_state") if entry else None
    }
    write_json(PRECHECK_PATH, precheck)

    if not entry:
        print("CONTROL_ACTION_UPDATE_LIVE_QUANTITY_FAILED")
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
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku_encoded}"

    get_response = requests.get(url, headers=headers, timeout=60)
    audit = {
        "status": "UNKNOWN",
        "decision": "control_action_update_live_quantity_started",
        "product_key": action["product_key"],
        "sku": sku,
        "requested_quantity": action["new_quantity"],
        "get_http_status": get_response.status_code,
        "put_http_status": None,
        "listing_state": entry.get("listing_state"),
        "pipeline_status": entry.get("pipeline_status"),
        "response_text": get_response.text[:4000]
    }

    if get_response.status_code != 200:
        audit["status"] = "ERROR"
        audit["decision"] = "inventory_item_read_failed"
        write_json(AUDIT_PATH, audit)
        print("CONTROL_ACTION_UPDATE_LIVE_QUANTITY_FAILED")
        print("decision = inventory_item_read_failed")
        print("product_key =", action["product_key"])
        print("sku =", sku)
        print("get_http_status =", get_response.status_code)
        return

    item = get_response.json()
    availability = item.get("availability")
    if not isinstance(availability, dict):
        availability = {}
        item["availability"] = availability
    ship = availability.get("shipToLocationAvailability")
    if not isinstance(ship, dict):
        ship = {}
        availability["shipToLocationAvailability"] = ship
    previous_quantity = ship.get("quantity")
    ship["quantity"] = int(action["new_quantity"])

    put_response = requests.put(url, headers=headers, json=item, timeout=60)
    audit["previous_quantity"] = previous_quantity
    audit["new_quantity"] = action["new_quantity"]
    audit["put_http_status"] = put_response.status_code
    audit["response_text"] = put_response.text[:4000]

    if put_response.status_code in (200, 201, 204):
        audit["status"] = "OK"
        audit["decision"] = "live_quantity_updated_via_registry"
        write_json(AUDIT_PATH, audit)
        print("CONTROL_ACTION_UPDATE_LIVE_QUANTITY_OK")
        print("decision = live_quantity_updated_via_registry")
        print("product_key =", action["product_key"])
        print("sku =", sku)
        print("previous_quantity =", previous_quantity)
        print("new_quantity =", action["new_quantity"])
        print("put_http_status =", put_response.status_code)
        return

    audit["status"] = "ERROR"
    audit["decision"] = "live_quantity_update_failed"
    write_json(AUDIT_PATH, audit)
    print("CONTROL_ACTION_UPDATE_LIVE_QUANTITY_FAILED")
    print("decision = live_quantity_update_failed")
    print("product_key =", action["product_key"])
    print("sku =", sku)
    print("put_http_status =", put_response.status_code)

if __name__ == "__main__":
    main()
