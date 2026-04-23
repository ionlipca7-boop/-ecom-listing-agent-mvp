import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REGISTRY_PATH = EXPORTS_DIR / "products_registry_v1.json"
AUDIT_PATH = EXPORTS_DIR / "registry_bootstrap_v1_audit.json"
def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "products": {
            "cable_001": {
                "sku": "ECOM-TEST-CABLE-001",
                "offerId": "152921341011"
            }
        }
    }
    REGISTRY_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {
        "status": "OK",
        "registry_path": str(REGISTRY_PATH),
        "products_count": len(data["products"]),
        "product_keys": list(data["products"].keys())
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REGISTRY_BOOTSTRAP_V1_OK")
    print("registry_path =", REGISTRY_PATH)
    print("products_count =", len(data["products"]))
    print("product_keys =", ", ".join(data["products"].keys()))
    print("audit_file =", AUDIT_PATH)
if __name__ == "__main__":
    main()
