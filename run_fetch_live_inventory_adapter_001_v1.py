import json
import requests
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
SECRET_DIR = BASE_DIR / "storage" / "secrets"
SKU = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
OUT_JSON = EXPORT_DIR / "adapter_001_live_inventory_fetch_v1.json"
def read_text(path):
    return path.read_text(encoding="utf-8").strip()
def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRET_DIR / "ebay_access_token.txt")
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{SKU}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }
    response = requests.get(url, headers=headers, timeout=60)
    raw_text = response.text
    try:
        data = response.json()
    except Exception:
        data = {"raw_text": raw_text}
    result = {
        "status": "OK" if response.status_code == 200 else "ERROR",
        "http_status": response.status_code,
        "sku": SKU,
        "url": url,
        "response": data
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("LIVE_INVENTORY_FETCH_V1")
    print("status =", result["status"])
    print("http_status =", result["http_status"])
    print("sku =", result["sku"])
if __name__ == "__main__":
    main()
