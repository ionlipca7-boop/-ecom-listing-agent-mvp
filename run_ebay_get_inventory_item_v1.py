import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SKU = "ECOM-TEST-CABLE-001"
API_URL = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + SKU
OUTPUT_FILE = EXPORTS_DIR / "ebay_get_inventory_item_audit_v1.json"

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Language": "de-DE"}
    response = requests.get(API_URL, headers=headers, timeout=60)
    try:
        data = response.json()
    except Exception:
        data = {"raw_text": response.text}
    result = {"http_status": response.status_code, "sku": SKU, "response_json": data}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("GET_INVENTORY_ITEM_V1_DONE")
    print("http_status =", response.status_code)
    print("sku =", SKU)

if __name__ == "__main__":
    main()
