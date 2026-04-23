import json
import re
import urllib.parse
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
MEMORY_PATH = EXPORTS_DIR / "recovery_memory_v1.json"
OFFER_PATH = EXPORTS_DIR / "real_offer_request_payload_v1.json"
AUDIT_PATH = EXPORTS_DIR / "real_inventory_check_or_create_audit_v1.json"
PRECHECK_PATH = EXPORTS_DIR / "inventory_precheck_v1.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"

DEFAULT_SKU = "USBCLadekabel2m60WSchnellladenDatenkabelq10p675"
DEFAULT_TITLE = "USB-C Ladekabel 2m 60W Schnellladen Datenkabel"
DEFAULT_DESCRIPTION = "Hochwertiges USB-C Ladekabel mit 60W Leistung fuer schnelles Laden und Datentransfer."
DEFAULT_QUANTITY = 10

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

def sanitize_sku(value):
    cleaned = re.sub(r"[^A-Za-z0-9]", "", str(value or ""))
    return cleaned[:50]

def resolve_runtime():
    offer_data = load_json(OFFER_PATH)
    payload = offer_data.get("payload", {}) if isinstance(offer_data, dict) else {}
    raw_sku = payload.get("sku") or offer_data.get("sku") or DEFAULT_SKU
    sanitized = sanitize_sku(raw_sku)
    final_sku = sanitized or DEFAULT_SKU
    quantity = payload.get("availableQuantity") or DEFAULT_QUANTITY
    return {
        "raw_sku": raw_sku,
        "sanitized_sku": sanitized,
        "sku": final_sku,
        "quantity": quantity,
        "title": DEFAULT_TITLE,
        "description": DEFAULT_DESCRIPTION
    }

def build_precheck(memory, runtime):
    return {
        "status": "OK",
        "decision": "inventory_precheck_completed",
        "action_name": "inventory",
        "raw_sku": runtime["raw_sku"],
        "sanitized_sku": runtime["sanitized_sku"],
        "final_sku": runtime["sku"],
        "known_failures": memory.get("known_failures", []),
        "working_paths": memory.get("working_paths", []),
        "cmd_traps": memory.get("cmd_traps", [])
    }

def make_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }

def build_create_payload(runtime):
    return {
        "availability": {
            "shipToLocationAvailability": {
                "quantity": int(runtime["quantity"])
            }
        },
        "condition": "NEW",
        "product": {
            "title": runtime["title"],
            "description": runtime["description"],
            "aspects": {
                "Marke": ["Markenlos"],
                "Typ": ["USB-C Ladekabel"],
                "Kabellaenge": ["2 m"],
                "Leistung": ["60W"]
            }
        }
    }

def main():
    memory = load_json(MEMORY_PATH)
    runtime = resolve_runtime()
    precheck = build_precheck(memory, runtime)
    write_json(PRECHECK_PATH, precheck)

    token = read_token(TOKEN_PATH)
    headers = make_headers(token)
    sku_encoded = urllib.parse.quote(runtime["sku"], safe="")
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku_encoded}"

    response = requests.get(url, headers=headers, timeout=60)
    audit = {
        "status": "UNKNOWN",
        "decision": "inventory_check_started",
        "raw_sku": runtime["raw_sku"],
        "sanitized_sku": runtime["sanitized_sku"],
        "sku": runtime["sku"],
        "get_http_status": response.status_code,
        "inventory_exists": False,
        "create_attempted": False,
        "create_http_status": None,
        "response_text": response.text[:4000]
    }

    if response.status_code == 200:
        audit["status"] = "OK"
        audit["decision"] = "inventory_item_exists"
        audit["inventory_exists"] = True
        write_json(AUDIT_PATH, audit)
        print("REAL_INVENTORY_ITEM_OK")
        print("decision = inventory_item_exists")
        print("sku =", runtime["sku"])
        print("get_http_status =", response.status_code)
        return

    if response.status_code == 404:
        payload = build_create_payload(runtime)
        create_response = requests.put(url, headers=headers, json=payload, timeout=60)
        audit["create_attempted"] = True
        audit["create_http_status"] = create_response.status_code
        audit["response_text"] = create_response.text[:4000]
        if create_response.status_code in (200, 201, 204):
            audit["status"] = "OK"
            audit["decision"] = "inventory_item_created"
            write_json(AUDIT_PATH, audit)
            print("REAL_INVENTORY_ITEM_OK")
            print("decision = inventory_item_created")
            print("sku =", runtime["sku"])
            print("create_http_status =", create_response.status_code)
            return
        audit["status"] = "ERROR"
        audit["decision"] = "inventory_item_create_failed"
        write_json(AUDIT_PATH, audit)
        print("REAL_INVENTORY_ITEM_FAILED")
        print("decision = inventory_item_create_failed")
        print("sku =", runtime["sku"])
        print("create_http_status =", create_response.status_code)
        return

    audit["status"] = "ERROR"
    audit["decision"] = "inventory_get_failed"
    write_json(AUDIT_PATH, audit)
    print("REAL_INVENTORY_ITEM_FAILED")
    print("decision = inventory_get_failed")
    print("sku =", runtime["sku"])
    print("get_http_status =", response.status_code)

if __name__ == "__main__":
    main()
