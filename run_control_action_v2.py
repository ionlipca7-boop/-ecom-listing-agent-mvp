import json
import subprocess
import requests
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_FILE = BASE_DIR / "storage" / "control_action.json"
OUTPUT_FILE = EXPORTS_DIR / "control_action_v2.json"
API_URL = "https://api.ebay.com/sell/inventory/v1/bulk_update_price_quantity"
LIVE_SKU = "ECOM-TEST-CABLE-001"
LIVE_OFFER_ID = "152921341011"
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
        result = {"status": "FAILED", "reason": "NO_CONTROL_ACTION_FILE"}
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CONTROL_ACTION_V2_DONE")
        print("status = FAILED")
        return
    control = read_json(INPUT_FILE)
    action = control.get("action", "")
    quantity = int(control.get("quantity", 0))
    refresh_run = subprocess.run(["python", "run_ebay_refresh_access_token_v2.py"])
    refresh_audit = read_json(EXPORTS_DIR / "ebay_refresh_access_token_audit_v2.json")
    refresh_ok = refresh_audit.get("status") == "OK" and refresh_audit.get("http_status") == 200
    api_status = "SKIPPED"
    api_http_status = None
    api_response = {}
    request_payload = {}
    if refresh_ok and action == "update_quantity" and quantity > 0:
        token = read_text(SECRETS_DIR / "ebay_access_token.txt")
        headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
        request_payload = {"requests": [{"sku": LIVE_SKU, "shipToLocationAvailability": {"quantity": quantity}, "offers": [{"offerId": LIVE_OFFER_ID, "availableQuantity": quantity}]}]}
        response = requests.post(API_URL, headers=headers, json=request_payload, timeout=60)
        api_response = safe_json(response)
        api_http_status = response.status_code
        api_status = "OK" if response.status_code == 200 else "FAILED"
    result = {"status": "OK" if refresh_ok and api_status == "OK" else "FAILED", "action": action, "quantity": quantity, "refresh_exit_code": refresh_run.returncode, "refresh_status": refresh_audit.get("status"), "refresh_http_status": refresh_audit.get("http_status"), "api_status": api_status, "api_http_status": api_http_status, "request_payload": request_payload, "api_response": api_response}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CONTROL_ACTION_V2_DONE")
    print("refresh_status =", refresh_audit.get("status"))
    print("refresh_http_status =", refresh_audit.get("http_status"))
    print("api_status =", api_status)
    print("api_http_status =", api_http_status)
if __name__ == "__main__":
    main()
