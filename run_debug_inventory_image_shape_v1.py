import json
from pathlib import Path

AUDIT_PATH = Path("storage/exports/control_action_get_live_status_audit_v2.json")

def main():
    data = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    snap = data.get("inventory_snapshot", {})
    product = snap.get("product", {}) if isinstance(snap, dict) else {}
    print("DEBUG_INVENTORY_IMAGE_SHAPE")
    print("top_level_keys =", list(snap.keys())[:30] if isinstance(snap, dict) else type(snap).__name__)
    print("product_type =", type(product).__name__)
    if isinstance(product, dict):
        print("product_keys =", list(product.keys())[:30])
        print("imageUrls_type =", type(product.get("imageUrls")).__name__)
        print("imageUrls_value =", product.get("imageUrls"))
        print("additionalImages_type =", type(product.get("additionalImages")).__name__)
        print("additionalImages_value =", product.get("additionalImages"))
        print("imageUrl_type =", type(product.get("imageUrl")).__name__)
        print("imageUrl_value =", product.get("imageUrl"))
    else:
        print("product_value =", product)

if __name__ == "__main__":
    main()
