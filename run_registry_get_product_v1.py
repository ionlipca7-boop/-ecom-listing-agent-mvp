import json
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REGISTRY_PATH = EXPORTS_DIR / "products_registry_v1.json"
AUDIT_PATH = EXPORTS_DIR / "registry_get_product_v1_audit.json"
DEFAULT_PRODUCT_KEY = "cable_001"
def main():
    product_key = sys.argv[1].strip() if len(sys.argv) > 1 else DEFAULT_PRODUCT_KEY
    if not REGISTRY_PATH.exists():
        audit = {
            "status": "REGISTRY_FILE_NOT_FOUND",
            "registry_path": str(REGISTRY_PATH),
            "product_key": product_key
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REGISTRY_GET_PRODUCT_V1_FAILED")
        print("reason = REGISTRY_FILE_NOT_FOUND")
        print("registry_path =", REGISTRY_PATH)
        return
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    products = data.get("products", {})
    item = products.get(product_key)
    if not item:
        audit = {
            "status": "PRODUCT_KEY_NOT_FOUND",
            "registry_path": str(REGISTRY_PATH),
            "product_key": product_key
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REGISTRY_GET_PRODUCT_V1_FAILED")
        print("reason = PRODUCT_KEY_NOT_FOUND")
        print("product_key =", product_key)
        return
    sku = str(item.get("sku", "")).strip()
    offer_id = str(item.get("offerId", "")).strip()
    status = "OK"
    if not sku and not offer_id:
        status = "EMPTY"
    elif not sku:
        status = "MISSING_SKU"
    elif not offer_id:
        status = "MISSING_OFFER_ID"
    audit = {
        "status": status,
        "registry_path": str(REGISTRY_PATH),
        "product_key": product_key,
        "sku": sku,
        "offerId": offer_id
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REGISTRY_GET_PRODUCT_V1_OK")
    print("product_key =", product_key)
    print("sku =", sku or "-")
    print("offerId =", offer_id or "-")
    print("status =", status)
    print("audit_file =", AUDIT_PATH)
if __name__ == "__main__":
    main()
