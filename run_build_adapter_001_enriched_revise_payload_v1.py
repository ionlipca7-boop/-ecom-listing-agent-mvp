import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def main():
    live_path = EXPORT_DIR / "adapter_001_live_inventory_item_v1.json"
    upgrade_path = EXPORT_DIR / "adapter_001_specifics_upgrade_v1.json"
    if not live_path.exists():
        raise FileNotFoundError("Missing live snapshot: " + str(live_path))
    if not upgrade_path.exists():
        raise FileNotFoundError("Missing specifics upgrade: " + str(upgrade_path))
    live = read_json(live_path)
    upgrade = read_json(upgrade_path)
    live_product = live.get("product", {})
    old_aspects = live_product.get("aspects", {})
    new_aspects = upgrade.get("recommended_item_specifics", {})
    merged_aspects = dict(old_aspects)
    merged_aspects.update(new_aspects)
    payload = {
        "sku": live.get("sku"),
        "locale": live.get("locale", "de_DE"),
        "product": dict(live_product),
        "condition": live.get("condition"),
        "availability": live.get("availability")
    }
    payload["product"]["aspects"] = merged_aspects
    result = {
        "status": "OK",
        "decision": "adapter_001_enriched_revise_payload_built",
        "product_key": "adapter_001",
        "sku": live.get("sku"),
        "offerId": upgrade.get("offerId"),
        "listingId": upgrade.get("listingId"),
        "old_aspects_count": len(old_aspects),
        "new_aspects_count": len(new_aspects),
        "merged_aspects_count": len(merged_aspects),
        "payload": payload
    }
    out_path = EXPORT_DIR / "adapter_001_enriched_revise_payload_v1.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_ENRICHED_REVISE_PAYLOAD_V1_OK")
    print("output =", str(out_path))
    print("decision =", result["decision"])
    print("merged_aspects_count =", result["merged_aspects_count"])
if __name__ == "__main__":
    main()
