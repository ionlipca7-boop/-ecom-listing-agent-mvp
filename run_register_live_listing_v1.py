import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REGISTRY_DIR = BASE_DIR / "storage" / "registry"

FINAL_AUDIT_PATH = EXPORTS_DIR / "final_live_publish_audit_v1.json"
LIVE_STATUS_PATH = EXPORTS_DIR / "live_listing_status_v1.json"
REGISTRY_PATH = REGISTRY_DIR / "live_listings_registry_v1.json"
AUDIT_PATH = EXPORTS_DIR / "live_listing_registry_audit_v1.json"

DEFAULT_PRODUCT_KEY = "cable_001"

def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    final_audit = load_json(FINAL_AUDIT_PATH, {})
    live_status = load_json(LIVE_STATUS_PATH, {})
    registry = load_json(REGISTRY_PATH, {"status":"OK","decision":"registry_initialized","items":[]})

    if not isinstance(registry, dict):
        registry = {"status":"OK","decision":"registry_rebuilt","items":[]}
    items = registry.get("items")
    if not isinstance(items, list):
        items = []

    entry = {
        "product_key": DEFAULT_PRODUCT_KEY,
        "sku": final_audit.get("sku"),
        "offerId": final_audit.get("offerId"),
        "listingId": final_audit.get("listingId"),
        "merchantLocationKey": final_audit.get("merchantLocationKey"),
        "listing_state": live_status.get("listing_state", "LIVE"),
        "pipeline_status": final_audit.get("pipeline_status"),
        "publish_http_status": final_audit.get("publish_http_status"),
        "source": "final_live_publish_audit_v1.json"
    }

    replaced = False
    new_items = []
    for item in items:
        if isinstance(item, dict) and item.get("product_key") == DEFAULT_PRODUCT_KEY:
            new_items.append(entry)
            replaced = True
        else:
            new_items.append(item)
    if not replaced:
        new_items.append(entry)

    registry["status"] = "OK"
    registry["decision"] = "live_listing_registered"
    registry["items"] = new_items
    registry["items_count"] = len(new_items)

    audit = {
        "status": "OK",
        "decision": "live_listing_registered",
        "product_key": DEFAULT_PRODUCT_KEY,
        "sku": entry["sku"],
        "offerId": entry["offerId"],
        "listingId": entry["listingId"],
        "merchantLocationKey": entry["merchantLocationKey"],
        "listing_state": entry["listing_state"],
        "pipeline_status": entry["pipeline_status"],
        "registry_items_count": len(new_items),
        "replaced_existing_product_key": replaced
    }

    write_json(REGISTRY_PATH, registry)
    write_json(AUDIT_PATH, audit)

    print("LIVE_LISTING_REGISTER_OK")
    print("product_key =", DEFAULT_PRODUCT_KEY)
    print("sku =", entry["sku"])
    print("offerId =", entry["offerId"])
    print("listingId =", entry["listingId"])
    print("registry_items_count =", len(new_items))

if __name__ == "__main__":
    main()
