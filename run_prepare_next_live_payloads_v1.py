import json
import sys
from pathlib import Path

EXPORTS_DIR = Path("storage") / "exports"
MERGED_FILE = EXPORTS_DIR / "ebay_next_merged_payload_v1.json"
INVENTORY_FILE = EXPORTS_DIR / "ebay_next_inventory_payload_v1.json"
OFFER_FILE = EXPORTS_DIR / "ebay_next_offer_payload_v1.json"
AUDIT_FILE = EXPORTS_DIR / "ebay_next_payload_prepare_audit_v1.json"

def find_placeholders(value, path="root"):
    found = []
    if isinstance(value, dict):
        for k, v in value.items():
            found.extend(find_placeholders(v, path + "." + str(k)))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            found.extend(find_placeholders(v, path + "[" + str(i) + "]"))
    elif isinstance(value, str):
        if "REPLACE_" in value:
            found.append({"path": path, "value": value})
    return found

def main():
    data = json.loads(MERGED_FILE.read_text(encoding="utf-8"))
    placeholders = find_placeholders(data)
    result = {
        "status": "READY" if not placeholders else "BLOCKED_BY_PLACEHOLDER",
        "placeholder_count": len(placeholders),
        "placeholders": placeholders
    }

    if not placeholders:
        inventory_payload = data["inventory_item"]
        offer_payload = data["offer"]
        INVENTORY_FILE.write_text(json.dumps(inventory_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        OFFER_FILE.write_text(json.dumps(offer_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        result["inventory_file"] = str(INVENTORY_FILE)
        result["offer_file"] = str(OFFER_FILE)
        result["sku"] = inventory_payload.get("sku")

    AUDIT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("PREPARE_NEXT_LIVE_PAYLOADS_V1_DONE")
    print("status =", result["status"])
    print("placeholder_count =", result["placeholder_count"])
    if placeholders:
        print("first_placeholder =", placeholders[0])
        sys.exit(1)
    print("sku =", result.get("sku"))

if __name__ == "__main__":
    main()
