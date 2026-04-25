import json
from pathlib import Path
import requests
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
SECRET_DIR = BASE_DIR / "storage" / "secrets"
def read_text(path):
    return path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
    token_path = SECRET_DIR / "ebay_access_token.txt"
    if not token_path.exists():
        raise FileNotFoundError("Missing token file: " + str(token_path))
    token = read_text(token_path)
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "Content-Language": "de-DE" 
    }
    response = requests.get(url, headers=headers, timeout=60)
    raw_text = response.text
    try:
        data = response.json() if raw_text.strip() else {}
    except Exception:
        data = {"raw_text": raw_text}
    snapshot_path = EXPORT_DIR / "adapter_001_live_inventory_item_v1.json"
    audit_path = EXPORT_DIR / "adapter_001_live_inventory_item_audit_v1.json"
    if response.status_code == 200:
        snapshot_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {
        "status": "OK" if response.status_code == 200 else "ERROR",
        "decision": "adapter_001_live_inventory_item_fetched" if response.status_code == 200 else "adapter_001_live_inventory_item_fetch_failed",
        "http_status": response.status_code,
        "product_key": "adapter_001",
        "sku": sku,
        "snapshot_file": str(snapshot_path),
        "top_level_keys": list(data.keys()) if isinstance(data, dict) else [],
        "response_body": data
    }
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    if response.status_code == 200:
        print("ADAPTER_001_LIVE_INVENTORY_ITEM_FETCH_OK")
    else:
        print("ADAPTER_001_LIVE_INVENTORY_ITEM_FETCH_FAILED")
    print("http_status =", response.status_code)
    print("sku =", sku)
    print("snapshot_file =", str(snapshot_path))
    print("audit_file =", str(audit_path))
if __name__ == "__main__":
    main()
