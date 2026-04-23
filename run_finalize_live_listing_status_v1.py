import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

INVENTORY_PATH = EXPORTS_DIR / "real_inventory_check_or_create_audit_v1.json"
LOCATION_PATH = EXPORTS_DIR / "resolved_merchant_location_key_v1.json"
OFFER_PATH = EXPORTS_DIR / "real_offer_create_audit_v2.json"
PUBLISH_PATH = EXPORTS_DIR / "real_offer_publish_audit_v1.json"
FINAL_AUDIT_PATH = EXPORTS_DIR / "final_live_publish_audit_v1.json"
LIVE_STATUS_PATH = EXPORTS_DIR / "live_listing_status_v1.json"

def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    inventory = load_json(INVENTORY_PATH)
    location = load_json(LOCATION_PATH)
    offer = load_json(OFFER_PATH)
    publish = load_json(PUBLISH_PATH)

    publish_json = publish.get("response_json", {}) if isinstance(publish.get("response_json"), dict) else {}

    sku = inventory.get("sku")
    merchant_location_key = location.get("merchantLocationKey")
    offer_id = offer.get("offerId")
    listing_id = publish_json.get("listingId")

    final_status = "LIVE_OK" if publish.get("status") == "OK" else "NOT_LIVE"

    final_audit = {
        "status": "OK" if final_status == "LIVE_OK" else "ERROR",
        "decision": "final_live_publish_recorded" if final_status == "LIVE_OK" else "final_live_publish_incomplete",
        "pipeline_status": final_status,
        "sku": sku,
        "merchantLocationKey": merchant_location_key,
        "offerId": offer_id,
        "listingId": listing_id,
        "inventory_status": inventory.get("status"),
        "inventory_decision": inventory.get("decision"),
        "offer_status": offer.get("status"),
        "offer_decision": offer.get("decision"),
        "publish_status": publish.get("status"),
        "publish_decision": publish.get("decision"),
        "publish_http_status": publish.get("http_status"),
        "publish_warnings": publish_json.get("warnings", []),
        "source_files": {
            "inventory": str(INVENTORY_PATH.name),
            "location": str(LOCATION_PATH.name),
            "offer": str(OFFER_PATH.name),
            "publish": str(PUBLISH_PATH.name)
        }
    }

    live_status = {
        "status": "OK" if final_status == "LIVE_OK" else "ERROR",
        "listing_state": "LIVE" if final_status == "LIVE_OK" else "UNKNOWN",
        "pipeline_status": final_status,
        "sku": sku,
        "offerId": offer_id,
        "listingId": listing_id,
        "merchantLocationKey": merchant_location_key
    }

    write_json(FINAL_AUDIT_PATH, final_audit)
    write_json(LIVE_STATUS_PATH, live_status)

    print("FINALIZE_LIVE_STATUS_OK")
    print("pipeline_status =", final_status)
    print("sku =", sku)
    print("offerId =", offer_id)
    print("listingId =", listing_id)

if __name__ == "__main__":
    main()
