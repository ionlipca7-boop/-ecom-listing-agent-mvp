import json
import sys
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SKU = "ECOM-TEST-CABLE-001"
API_URL = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + SKU
OUTPUT_FILE = EXPORTS_DIR / "ebay_create_inventory_item_audit_v6.json"

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {"raw_text": response.text}

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    image_url = read_text(SECRETS_DIR / "ebay_test_image_url.txt")

    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Content-Language": "de-DE",
    }

    payload = {
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 10
            }
        },
        "condition": "NEW",
        "product": {
            "title": "USB-C Ladekabel 2m 60W Schnellladen",
            "description": "USB-C Kabel 2m fuer Schnellladen und Datentransfer.",
            "imageUrls": [image_url],
            "brand": "Markenlos",
            "mpn": "Nicht zutreffend",
            "aspects": {
                "Produktart": ["USB-Kabel"],
                "Marke": ["Markenlos"],
                "Herstellernummer": ["Nicht zutreffend"]
            }
        }
    }

    response = requests.put(API_URL, headers=headers, json=payload, timeout=60)
    data = safe_json(response)

    result = {
        "status": "OK" if response.status_code == 204 else "FAILED",
        "http_status": response.status_code,
        "sku": SKU,
        "request_payload": payload,
        "response_json": data,
    }

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("CREATE_INVENTORY_ITEM_V6_DONE")
    print("http_status =", response.status_code)
    print("sku =", SKU)
    if response.status_code != 204:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
