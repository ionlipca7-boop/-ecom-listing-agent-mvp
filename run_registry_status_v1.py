import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REGISTRY_PATH = EXPORTS_DIR / "products_registry_v1.json"
AUDIT_PATH = EXPORTS_DIR / "registry_status_v1_audit.json"
def main():
    if not REGISTRY_PATH.exists():
        audit = {
            "status": "REGISTRY_FILE_NOT_FOUND",
            "registry_path": str(REGISTRY_PATH),
            "products_count": 0,
            "items": []
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REGISTRY_STATUS_V1_FAILED")
        print("reason = REGISTRY_FILE_NOT_FOUND")
        print("registry_path =", REGISTRY_PATH)
        return
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    products = data.get("products", {})
    items = []
    print("REGISTRY_STATUS_V1")
    print("registry_path =", REGISTRY_PATH)
    print("products_count =", len(products))
    for product_key, info in products.items():
        sku = str(info.get("sku", "")).strip()
        offer_id = str(info.get("offerId", "")).strip()
        if sku and offer_id:
            item_status = "OK"
        elif sku and not offer_id:
            item_status = "MISSING_OFFER_ID"
        elif not sku and offer_id:
            item_status = "MISSING_SKU"
        else:
            item_status = "EMPTY"
        item = {
            "product_key": product_key,
            "sku": sku,
            "offerId": offer_id,
            "status": item_status
        }
        items.append(item)
        print("---")
        print("product_key =", product_key)
        print("sku =", sku or "-")
        print("offerId =", offer_id or "-")
        print("status =", item_status)
    overall_status = "OK"
    if not products:
        overall_status = "EMPTY_REGISTRY"
    elif any(x["status"] != "OK" for x in items):
        overall_status = "PARTIAL"
    audit = {
        "status": overall_status,
        "registry_path": str(REGISTRY_PATH),
        "products_count": len(products),
        "items": items
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("---")
    print("audit_status =", overall_status)
    print("audit_file =", AUDIT_PATH)
if __name__ == "__main__":
    main()
