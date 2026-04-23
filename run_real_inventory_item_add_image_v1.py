import json
import urllib.parse
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
MEMORY_PATH = EXPORTS_DIR / "recovery_memory_v1.json"
INVENTORY_AUDIT_PATH = EXPORTS_DIR / "real_inventory_check_or_create_audit_v1.json"
PRECHECK_PATH = EXPORTS_DIR / "real_inventory_item_add_image_precheck_v1.json"
AUDIT_PATH = EXPORTS_DIR / "real_inventory_item_add_image_audit_v1.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"

DEFAULT_SKU = "USBCLadekabel2m60WSchnellladenDatenkabelq10p675"
IMAGE_URL = "https://i.ebayimg.com/images/g/tkoAAeSwFOBpuYyi/s-l1600.webp"

def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def read_token(path):
    token = path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
    if not token:
        raise ValueError("Access token file is empty")
    return token

def resolve_sku():
    data = load_json(INVENTORY_AUDIT_PATH)
    sku = str(data.get("sku") or DEFAULT_SKU).strip()
    if not sku:
        raise ValueError("SKU not found")
    return sku

def build_precheck(memory, sku):
    return {
        "status": "OK",
        "decision": "inventory_item_add_image_precheck_completed",
        "action_name": "inventory_item_add_image",
        "sku": sku,
        "image_url": IMAGE_URL,
        "known_failures": memory.get("known_failures", []),
        "working_paths": memory.get("working_paths", []),
        "cmd_traps": memory.get("cmd_traps", [])
    }

def main():
    memory = load_json(MEMORY_PATH)
    sku = resolve_sku()
    precheck = build_precheck(memory, sku)
    write_json(PRECHECK_PATH, precheck)

    token = read_token(TOKEN_PATH)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }

    sku_encoded = urllib.parse.quote(sku, safe="")
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku_encoded}"

    get_response = requests.get(url, headers=headers, timeout=60)
    audit = {
        "status": "UNKNOWN",
        "decision": "inventory_item_image_read_started",
        "sku": sku,
        "image_url": IMAGE_URL,
        "get_http_status": get_response.status_code,
        "put_http_status": None,
        "response_text": get_response.text[:4000]
    }

    if get_response.status_code != 200:
        audit["status"] = "ERROR"
        audit["decision"] = "inventory_item_image_read_failed"
        write_json(AUDIT_PATH, audit)
        print("REAL_INVENTORY_ITEM_IMAGE_FAILED")
        print("decision = inventory_item_image_read_failed")
        print("sku =", sku)
        print("get_http_status =", get_response.status_code)
        return

    item = get_response.json()
    product = item.get("product")
    if not isinstance(product, dict):
        product = {}
        item["product"] = product
    existing = product.get("imageUrls")
    if not isinstance(existing, list):
        existing = []
    cleaned = []
    for x in existing:
        if isinstance(x, str) and x.strip():
            cleaned.append(x.strip())
    if IMAGE_URL not in cleaned:
        cleaned.append(IMAGE_URL)
    product["imageUrls"] = cleaned

    put_response = requests.put(url, headers=headers, json=item, timeout=60)
    audit["put_http_status"] = put_response.status_code
    audit["updated_image_count"] = len(cleaned)
    audit["updated_item"] = item
    audit["response_text"] = put_response.text[:4000]

    if put_response.status_code in (200, 201, 204):
        audit["status"] = "OK"
        audit["decision"] = "inventory_item_image_updated"
        write_json(AUDIT_PATH, audit)
        print("REAL_INVENTORY_ITEM_IMAGE_OK")
        print("decision = inventory_item_image_updated")
        print("sku =", sku)
        print("put_http_status =", put_response.status_code)
        print("updated_image_count =", len(cleaned))
        return

    audit["status"] = "ERROR"
    audit["decision"] = "inventory_item_image_update_failed"
    write_json(AUDIT_PATH, audit)
    print("REAL_INVENTORY_ITEM_IMAGE_FAILED")
    print("decision = inventory_item_image_update_failed")
    print("sku =", sku)
    print("put_http_status =", put_response.status_code)

if __name__ == "__main__":
    main()
