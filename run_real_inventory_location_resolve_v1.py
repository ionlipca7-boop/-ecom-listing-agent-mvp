import json
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
MEMORY_PATH = EXPORTS_DIR / "recovery_memory_v1.json"
PRECHECK_PATH = EXPORTS_DIR / "inventory_location_precheck_v1.json"
AUDIT_PATH = EXPORTS_DIR / "real_inventory_location_resolve_audit_v1.json"
RESOLVED_PATH = EXPORTS_DIR / "resolved_merchant_location_key_v1.json"
TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"

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

def build_precheck(memory):
    return {
        "status": "OK",
        "decision": "inventory_location_precheck_completed",
        "action_name": "inventory_location_resolve",
        "known_failures": memory.get("known_failures", []),
        "working_paths": memory.get("working_paths", []),
        "cmd_traps": memory.get("cmd_traps", [])
    }

def pick_location(locations):
    if not isinstance(locations, list):
        return None
    for item in locations:
        if not isinstance(item, dict):
            continue
        key = item.get("merchantLocationKey")
        enabled = item.get("enabled")
        if key and enabled is True:
            return item
    for item in locations:
        if not isinstance(item, dict):
            continue
        key = item.get("merchantLocationKey")
        if key:
            return item
    return None

def main():
    memory = load_json(MEMORY_PATH)
    precheck = build_precheck(memory)
    write_json(PRECHECK_PATH, precheck)

    token = read_token(TOKEN_PATH)
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }

    response = requests.get("https://api.ebay.com/sell/inventory/v1/location", headers=headers, timeout=60)

    audit = {
        "status": "UNKNOWN",
        "decision": "inventory_location_list_checked",
        "http_status": response.status_code,
        "resolved_merchantLocationKey": None,
        "locations_count": 0,
        "response_text": response.text[:4000]
    }

    try:
        data = response.json()
    except Exception:
        data = None

    if data is not None:
        audit["response_json"] = data

    if response.status_code != 200:
        audit["status"] = "ERROR"
        audit["decision"] = "inventory_location_list_failed"
        write_json(AUDIT_PATH, audit)
        print("REAL_INVENTORY_LOCATION_FAILED")
        print("decision = inventory_location_list_failed")
        print("http_status =", response.status_code)
        return

    locations = []
    if isinstance(data, dict):
        locations = data.get("locations", []) or []
    audit["locations_count"] = len(locations)
    chosen = pick_location(locations)

    if chosen is None:
        audit["status"] = "ERROR"
        audit["decision"] = "no_inventory_location_found"
        write_json(AUDIT_PATH, audit)
        print("REAL_INVENTORY_LOCATION_FAILED")
        print("decision = no_inventory_location_found")
        print("http_status =", response.status_code)
        print("locations_count =", len(locations))
        return

    resolved = {
        "status": "OK",
        "decision": "merchant_location_key_resolved",
        "merchantLocationKey": chosen.get("merchantLocationKey"),
        "enabled": chosen.get("enabled"),
        "name": chosen.get("name"),
        "locationTypes": chosen.get("locationTypes"),
        "location": chosen.get("location")
    }
    write_json(RESOLVED_PATH, resolved)

    audit["status"] = "OK"
    audit["decision"] = "inventory_location_resolved"
    audit["resolved_merchantLocationKey"] = chosen.get("merchantLocationKey")
    write_json(AUDIT_PATH, audit)

    print("REAL_INVENTORY_LOCATION_OK")
    print("decision = inventory_location_resolved")
    print("merchantLocationKey =", chosen.get("merchantLocationKey"))
    print("locations_count =", len(locations))

if __name__ == "__main__":
    main()
