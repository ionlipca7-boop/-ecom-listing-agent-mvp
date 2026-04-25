import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REGISTRY_PATH = EXPORTS_DIR / "products_registry_v1.json"
ACTION_PATH = EXPORTS_DIR / "control_action_v4.json"
AUDIT_PATH = EXPORTS_DIR / "registry_resolve_action_v1_audit.json"
def main():
    if not REGISTRY_PATH.exists():
        audit = {
            "status": "REGISTRY_FILE_NOT_FOUND",
            "registry_path": str(REGISTRY_PATH)
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REGISTRY_RESOLVE_ACTION_V1_FAILED")
        print("reason = REGISTRY_FILE_NOT_FOUND")
        return
    if not ACTION_PATH.exists():
        audit = {
            "status": "ACTION_FILE_NOT_FOUND",
            "action_path": str(ACTION_PATH)
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REGISTRY_RESOLVE_ACTION_V1_FAILED")
        print("reason = ACTION_FILE_NOT_FOUND")
        return
    registry_data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    action_data = json.loads(ACTION_PATH.read_text(encoding="utf-8"))
    products = registry_data.get("products", {})
    actions = action_data.get("actions", [])
    if not actions:
        audit = {
            "status": "NO_ACTIONS",
            "action_path": str(ACTION_PATH),
            "resolved_count": 0,
            "resolved_actions": []
        }
        AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("REGISTRY_RESOLVE_ACTION_V1_FAILED")
        print("reason = NO_ACTIONS")
        return
    resolved_actions = []
    overall_status = "OK"
    print("REGISTRY_RESOLVE_ACTION_V1")
    print("action_path =", ACTION_PATH)
    print("actions_count =", len(actions))
    for action in actions:
        action_name = str(action.get("action", "")).strip()
        product_key = str(action.get("product_key", "")).strip()
        quantity = action.get("quantity")
        product = products.get(product_key, {})
        sku = str(product.get("sku", "")).strip()
        offer_id = str(product.get("offerId", "")).strip()
        item_status = "OK"
        if not product_key:
            item_status = "MISSING_PRODUCT_KEY"
        elif not product:
            item_status = "PRODUCT_NOT_FOUND"
        elif not sku and not offer_id:
            item_status = "EMPTY_PRODUCT_DATA"
        elif not sku:
            item_status = "MISSING_SKU"
        elif not offer_id:
            item_status = "MISSING_OFFER_ID"
        if item_status != "OK":
            overall_status = "PARTIAL"
        resolved = {
            "action": action_name,
            "product_key": product_key,
            "quantity": quantity,
            "sku": sku,
            "offerId": offer_id,
            "status": item_status
        }
        resolved_actions.append(resolved)
        print("---")
        print("action =", action_name)
        print("product_key =", product_key or "-")
        print("quantity =", quantity)
        print("sku =", sku or "-")
        print("offerId =", offer_id or "-")
        print("status =", item_status)
    audit = {
        "status": overall_status,
        "registry_path": str(REGISTRY_PATH),
        "action_path": str(ACTION_PATH),
        "resolved_count": len(resolved_actions),
        "resolved_actions": resolved_actions
    }
    AUDIT_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("---")
    print("audit_status =", overall_status)
    print("audit_file =", AUDIT_PATH)
if __name__ == "__main__":
    main()
