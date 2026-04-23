import json
import re
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
MEMORY_PATH = EXPORTS_DIR / "recovery_memory_v1.json"
OFFER_SOURCE_PATH = EXPORTS_DIR / "real_offer_request_payload_v1.json"
INVENTORY_AUDIT_PATH = EXPORTS_DIR / "real_inventory_check_or_create_audit_v1.json"
LOCATION_PATH = EXPORTS_DIR / "resolved_merchant_location_key_v1.json"
PRECHECK_PATH = EXPORTS_DIR / "real_offer_create_precheck_v2.json"
AUDIT_PATH = EXPORTS_DIR / "real_offer_create_audit_v2.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"

CATEGORY_ID = "44932"
MARKETPLACE_ID = "EBAY_DE"
FULFILLMENT_POLICY_ID = "257755855024"
PAYMENT_POLICY_ID = "257755913024"
RETURN_POLICY_ID = "257755877024"
DEFAULT_PRICE = "6.75"
DEFAULT_QUANTITY = 10
DEFAULT_SKU = "USBCLadekabel2m60WSchnellladenDatenkabelq10p675"
DEFAULT_LOCATION_KEY = "ECOM_DE_LOC_1"

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
    source = load_json(OFFER_SOURCE_PATH)
    inv = load_json(INVENTORY_AUDIT_PATH)
    loc = load_json(LOCATION_PATH)
    payload = source.get("payload", {}) if isinstance(source, dict) else {}
    raw_sku = inv.get("sku") or payload.get("sku") or source.get("sku") or DEFAULT_SKU
    sku = sanitize_sku(raw_sku) or DEFAULT_SKU
    raw_price = payload.get("pricingSummary", {}).get("price", {}).get("value", DEFAULT_PRICE)
    price = str(raw_price or DEFAULT_PRICE)
    quantity = payload.get("availableQuantity") or DEFAULT_QUANTITY
    merchant_location_key = loc.get("merchantLocationKey") or DEFAULT_LOCATION_KEY
    return {
        "raw_sku": raw_sku,
        "sku": sku,
        "price": price,
        "quantity": quantity,
        "merchantLocationKey": merchant_location_key
    }

def build_precheck(memory, runtime):
    return {
        "status": "OK",
        "decision": "real_offer_create_precheck_completed",
        "action_name": "real_offer_create",
        "sku": runtime["sku"],
        "price": runtime["price"],
        "quantity": runtime["quantity"],
        "merchantLocationKey": runtime["merchantLocationKey"],
        "known_failures": memory.get("known_failures", []),
        "working_paths": memory.get("working_paths", []),
        "cmd_traps": memory.get("cmd_traps", [])
    }

def build_payload(runtime):
    return {
        "sku": runtime["sku"],
        "marketplaceId": MARKETPLACE_ID,
        "format": "FIXED_PRICE",
        "availableQuantity": int(runtime["quantity"]),
        "categoryId": CATEGORY_ID,
        "merchantLocationKey": runtime["merchantLocationKey"],
        "pricingSummary": {
            "price": {
                "value": runtime["price"],
                "currency": "EUR"
            }
        },
        "listingPolicies": {
            "fulfillmentPolicyId": FULFILLMENT_POLICY_ID,
            "paymentPolicyId": PAYMENT_POLICY_ID,
            "returnPolicyId": RETURN_POLICY_ID
        }
    }

def main():
    memory = load_json(MEMORY_PATH)
    runtime = resolve_runtime()
    precheck = build_precheck(memory, runtime)
    write_json(PRECHECK_PATH, precheck)

    token = read_token(TOKEN_PATH)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }

    payload = build_payload(runtime)
    response = requests.post("https://api.ebay.com/sell/inventory/v1/offer", headers=headers, json=payload, timeout=60)

    audit = {
        "status": "UNKNOWN",
        "decision": "real_offer_create_sent",
        "sku": runtime["sku"],
        "merchantLocationKey": runtime["merchantLocationKey"],
        "http_status": response.status_code,
        "request_payload": payload,
        "response_text": response.text[:4000]
    }

    try:
        response_json = response.json()
    except Exception:
        response_json = None

    if response_json is not None:
        audit["response_json"] = response_json
        if isinstance(response_json, dict) and "offerId" in response_json:
            audit["offerId"] = response_json.get("offerId")

    if response.status_code in (200, 201):
        audit["status"] = "OK"
        audit["decision"] = "real_offer_created"
        write_json(AUDIT_PATH, audit)
        print("REAL_OFFER_CREATE_OK")
        print("decision = real_offer_created")
        print("sku =", runtime["sku"])
        print("merchantLocationKey =", runtime["merchantLocationKey"])
        print("http_status =", response.status_code)
        print("offerId =", audit.get("offerId"))
        return

    audit["status"] = "ERROR"
    audit["decision"] = "real_offer_create_failed"
    write_json(AUDIT_PATH, audit)
    print("REAL_OFFER_CREATE_FAILED")
    print("decision = real_offer_create_failed")
    print("sku =", runtime["sku"])
    print("merchantLocationKey =", runtime["merchantLocationKey"])
    print("http_status =", response.status_code)

if __name__ == "__main__":
    main()
