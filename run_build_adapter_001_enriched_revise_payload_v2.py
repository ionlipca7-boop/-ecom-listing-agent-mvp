import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def main():
    payload_v1_path = EXPORT_DIR / "adapter_001_enriched_revise_payload_v1.json"
    images_path = EXPORT_DIR / "adapter_001_image_urls_v3.json"
    if not payload_v1_path.exists():
        raise FileNotFoundError("Missing file: " + str(payload_v1_path))
    if not images_path.exists():
        raise FileNotFoundError("Missing file: " + str(images_path))
    d1 = read_json(payload_v1_path)
    d2 = read_json(images_path)
    payload = d1["payload"]
    product = payload.get("product", {})
    image_urls = d2.get("imageUrls", [])
    product["imageUrls"] = image_urls
    payload["product"] = product
    result = {
        "status": "OK",
        "decision": "adapter_001_enriched_revise_payload_v2_built",
        "product_key": "adapter_001",
        "sku": payload.get("sku"),
        "offerId": d1.get("offerId"),
        "listingId": d1.get("listingId"),
        "image_urls_count": len(image_urls),
        "aspects_count": len(payload.get("product", {}).get("aspects", {})),
        "payload": payload
    }
    out_path = EXPORT_DIR / "adapter_001_enriched_revise_payload_v2.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_ENRICHED_REVISE_PAYLOAD_V2_OK")
    print("output =", str(out_path))
    print("decision =", result["decision"])
    print("image_urls_count =", result["image_urls_count"])
if __name__ == "__main__":
    main()
