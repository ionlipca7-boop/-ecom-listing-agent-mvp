import json
from pathlib import Path
from datetime import datetime, UTC

INVENTORY_FILE = Path("ebay_inventory_payload_v1.json")
OFFER_FILE = Path("ebay_offer_payload_v1.json")
LOCATION_FILE = Path("ebay_location_payload_v1.json")

OUTPUT_FILE = Path("ebay_publish_mock_result_v1.json")


def _utc_now():
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _read_json(path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    inventory = _read_json(INVENTORY_FILE)
    offer = _read_json(OFFER_FILE)
    location = _read_json(LOCATION_FILE)

    missing = []

    if not inventory:
        missing.append("inventory")
    if not offer:
        missing.append("offer")
    if not location:
        missing.append("location")

    if missing:
        result = {
            "status": "FAILED",
            "missing": missing,
            "message": "Missing required payloads"
        }
    else:
        result = {
            "status": "READY_FOR_PUBLISH",
            "mode": "FULL_PIPELINE_READY",
            "timestamp": _utc_now(),
            "summary": {
                "inventory": "OK",
                "offer": "OK",
                "location": "OK"
            },
            "next_step": "CONNECT_REAL_EBAY_API"
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("PUBLISH MOCK EXECUTOR:")
    print(f"status: {result['status']}")
    print(f"output_file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()