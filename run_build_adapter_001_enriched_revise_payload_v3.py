import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def main():
    live_path = EXPORT_DIR / "adapter_001_live_inventory_item_v1.json"
    payload_v2_path = EXPORT_DIR / "adapter_001_enriched_revise_payload_v2.json"
    if not live_path.exists():
        raise FileNotFoundError("Missing file: " + str(live_path))
    if not payload_v2_path.exists():
        raise FileNotFoundError("Missing file: " + str(payload_v2_path))
    live = read_json(live_path)
    d2 = read_json(payload_v2_path)
    payload = d2["payload"]
    product = payload.get("product", {})
    product["title"] = "USB-C auf USB-A OTG Adapter USB 3.0 Typ C Datenadapter Schwarz"
    product["description"] = "Kompakter USB-C auf USB-A OTG Adapter fuer schnelles und stabiles Verbinden Ihrer Geraete. Geeignet fuer Datenuebertragung und den Alltag zu Hause, im Auto oder auf Reisen. Farbe: Schwarz. USB Standard: USB 3.0."
    payload["product"] = product
    result = {
        "status": "OK",
        "decision": "adapter_001_enriched_revise_payload_v3_built",
        "product_key": "adapter_001",
        "sku": payload.get("sku"),
        "offerId": d2.get("offerId"),
        "listingId": d2.get("listingId"),
        "image_urls_count": len(product.get("imageUrls", [])),
        "aspects_count": len(product.get("aspects", {})),
        "has_title": bool(product.get("title")),
        "has_description": bool(product.get("description")),
        "payload": payload
    }
    out_path = EXPORT_DIR / "adapter_001_enriched_revise_payload_v3.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_ENRICHED_REVISE_PAYLOAD_V3_OK")
    print("output =", str(out_path))
    print("decision =", result["decision"])
    print("has_title =", result["has_title"])
    print("has_description =", result["has_description"])
if __name__ == "__main__":
    main()
