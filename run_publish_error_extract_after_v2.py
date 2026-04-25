import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILE = BASE_DIR / "storage" / "exports" / "publish_existing_offer_repair_v2.json"

def main():
    data = json.loads(FILE.read_text(encoding="utf-8"))
    print("PUBLISH_ERROR_AFTER_V2")
    print("status =", data.get("status"))
    print("decision =", data.get("decision"))
    print("product_key =", data.get("product_key"))
    print("sku =", data.get("sku"))
    print("offerId =", data.get("offerId"))
    print("publish_http_status =", data.get("publish_http_status"))
    print("publish_response =")
    print(json.dumps(data.get("publish_response", data.get("publish_response_text")), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
