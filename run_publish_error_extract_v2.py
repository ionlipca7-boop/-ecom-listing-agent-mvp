import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILES = [
    BASE_DIR / "storage" / "exports" / "full_publish_pipeline_v2_audit.json",
    BASE_DIR / "storage" / "exports" / "publish_existing_offer_repair_v1.json",
    BASE_DIR / "storage" / "exports" / "new_product_adapter_001.json"
]

def main():
    print("PUBLISH_ERROR_EXTRACT_V2")
    for path in FILES:
        if not path.exists():
            print("file_missing =", path.name)
            print("---")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        print("file =", path.name)
        if path.name == "new_product_adapter_001.json":
            print("product_key =", data.get("product_key"))
            print("title =", data.get("title") or data.get("main_title"))
            print("condition =", data.get("condition"))
            print("price =", data.get("price") or data.get("price_eur"))
            print("imageUrls =", json.dumps(data.get("imageUrls") or data.get("image_urls"), ensure_ascii=False))
            print("aspects =", json.dumps(data.get("aspects"), ensure_ascii=False))
            print("brand =", data.get("brand"))
            print("mpn =", data.get("mpn"))
        else:
            print("status =", data.get("status"))
            print("decision =", data.get("decision"))
            print("offerId =", data.get("offerId"))
            print("publish_http_status =", data.get("publish_http_status"))
            print("publish_response =")
            print(json.dumps(data.get("publish_response", data.get("publish_response_text")), ensure_ascii=False, indent=2))
        print("---")

if __name__ == "__main__":
    main()
