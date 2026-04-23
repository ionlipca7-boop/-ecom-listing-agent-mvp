import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIT_FILE = BASE_DIR / "storage" / "exports" / "full_publish_pipeline_v2_audit.json"
INPUT_FILE = BASE_DIR / "storage" / "exports" / "new_product_adapter_001.json"

def main():
    audit = json.loads(AUDIT_FILE.read_text(encoding="utf-8"))
    product = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    print("PUBLISH_FAILURE_AUDIT")
    print("status =", audit.get("status"))
    print("decision =", audit.get("decision"))
    print("product_key =", audit.get("product_key"))
    print("sku =", audit.get("sku"))
    print("offerId =", audit.get("offerId"))
    print("publish_http_status =", audit.get("publish_http_status"))
    print("input_title =", product.get("title") or product.get("main_title"))
    print("input_condition =", product.get("condition"))
    print("input_price =", product.get("price") or product.get("price_eur"))
    print("input_imageUrls =", product.get("imageUrls") or product.get("image_urls"))
    print("input_aspects =", json.dumps(product.get("aspects"), ensure_ascii=False))
    print("inventory_payload =")
    print(json.dumps(audit.get("inventory_payload"), ensure_ascii=False, indent=2))
    print("offer_payload =")
    print(json.dumps(audit.get("offer_payload"), ensure_ascii=False, indent=2))
    print("publish_response =")
    print(json.dumps(audit.get("publish_response", audit.get("publish_response_text")), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
