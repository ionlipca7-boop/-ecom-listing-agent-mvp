import json
import subprocess
import requests
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
STORAGE_DIR = BASE_DIR / "storage"
EXPORTS_DIR = STORAGE_DIR / "exports"
INPUT_FILE = STORAGE_DIR / "control_actions_v4.json"
REGISTRY_FILE = STORAGE_DIR / "products_registry_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "control_action_v4.json"
API_URL = "https://api.ebay.com/sell/inventory/v1/bulk_update_price_quantity"
def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {"raw_text": response.text}
def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    if not INPUT_FILE.exists():
        result = {"status": "FAILED", "reason": "NO_CONTROL_ACTIONS_FILE"}
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CONTROL_ACTION_V4_DONE")
        print("status = FAILED")
        return
    if not REGISTRY_FILE.exists():
        result = {"status": "FAILED", "reason": "NO_REGISTRY_FILE"}
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CONTROL_ACTION_V4_DONE")
        print("status = FAILED")
        return
    control = read_json(INPUT_FILE)
    registry = read_json(REGISTRY_FILE).get("products", {})
    actions = control.get("actions", [])
    refresh_run = subprocess.run(["python", "run_ebay_refresh_access_token_v2.py"])
    refresh_audit = read_json(EXPORTS_DIR / "ebay_refresh_access_token_audit_v2.json")
    refresh_ok = refresh_audit.get("status") == "OK" and refresh_audit.get("http_status") == 200
    token = read_text(SECRETS_DIR / "ebay_access_token.txt") if refresh_ok else ""
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"} if refresh_ok else {}
    results = []
    overall_ok = refresh_ok
    for item in actions:
        action = item.get("action", "")
        product_key = item.get("product_key", "")
        quantity = int(item.get("quantity", 0))
        reg = registry.get(product_key, {})
        sku = reg.get("sku", "")
        offer_id = reg.get("offerId", "")
        if not refresh_ok:
            results.append({"action": action, "product_key": product_key, "status": "SKIPPED", "http_status": None, "response_json": {"reason": "REFRESH_FAILED"}})
            overall_ok = False
            continue
        if action == "update_quantity" and product_key and sku and offer_id and quantity > 0:
            payload = {"requests": [{"sku": sku, "shipToLocationAvailability": {"quantity": quantity}, "offers": [{"offerId": offer_id, "availableQuantity": quantity}]}]}
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            data = safe_json(response)
            item_status = "OK" if response.status_code == 200 else "FAILED"
            if response.status_code != 200: overall_ok = False
            results.append({"action": action, "product_key": product_key, "sku": sku, "offerId": offer_id, "quantity": quantity, "status": item_status, "http_status": response.status_code, "request_payload": payload, "response_json": data})
        else:
            results.append({"action": action, "product_key": product_key, "sku": sku, "offerId": offer_id, "quantity": quantity, "status": "FAILED", "http_status": None, "response_json": {"reason": "INVALID_ACTION_OR_REGISTRY_DATA"}})
            overall_ok = False
    result = {"status": "OK" if overall_ok else "FAILED", "refresh_exit_code": refresh_run.returncode, "refresh_status": refresh_audit.get("status"), "refresh_http_status": refresh_audit.get("http_status"), "actions_count": len(actions), "results": results}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CONTROL_ACTION_V4_DONE")
    print("refresh_status =", refresh_audit.get("status"))
    print("refresh_http_status =", refresh_audit.get("http_status"))
    print("actions_count =", len(actions))
    print("status =", "OK" if overall_ok else "FAILED")
if __name__ == "__main__":
    main()
