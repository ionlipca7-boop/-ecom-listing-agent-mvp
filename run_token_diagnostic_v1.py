import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
API_URL = "https://api.ebay.com/sell/inventory/v1/bulk_update_price_quantity"
LIVE_SKU = "ECOM-TEST-CABLE-001"
LIVE_OFFER_ID = "152921341011"
TEST_TOTAL_QTY = 20
TEST_OFFER_QTY = 20
OUTPUT_FILE = EXPORTS_DIR / "ebay_token_diagnostic_v1.json"
TOKEN_FILES = [
    "ebay_access_token.txt",
    "ebay_user_token.txt",
    "ebay_user_token_prev_backup_2.txt",
    "ebay_user_token_with_spaces_backup.txt",
    "ebay_user_token_bad_backup.txt",
    "ebay_refresh_token.txt",
]

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {"raw_text": response.text}

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"requests": [{"sku": LIVE_SKU, "shipToLocationAvailability": {"quantity": TEST_TOTAL_QTY}, "offers": [{"offerId": LIVE_OFFER_ID, "availableQuantity": TEST_OFFER_QTY}]}]}
    results = []
    for name in TOKEN_FILES:
        path = SECRETS_DIR / name
        if not path.exists():
            results.append({"file": name, "exists": False})
            continue
        token = read_text(path)
        headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            data = safe_json(response)
            results.append({"file": name, "exists": True, "length": len(token), "http_status": response.status_code, "response_json": data})
            print("CHECKED", name, "status =", response.status_code)
        except Exception as e:
            results.append({"file": name, "exists": True, "length": len(token), "exception": str(e)})
            print("CHECKED", name, "exception")
    OUTPUT_FILE.write_text(json.dumps({"status": "DONE", "results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TOKEN_DIAGNOSTIC_V1_DONE")
    print("output_file =", OUTPUT_FILE)

if __name__ == "__main__":
    main()
