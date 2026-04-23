import json
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
MEMORY_PATH = EXPORTS_DIR / "recovery_memory_v1.json"
OFFER_AUDIT_PATH = EXPORTS_DIR / "real_offer_create_audit_v2.json"
PRECHECK_PATH = EXPORTS_DIR / "real_offer_publish_precheck_v1.json"
AUDIT_PATH = EXPORTS_DIR / "real_offer_publish_audit_v1.json"
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

def resolve_runtime():
    offer_audit = load_json(OFFER_AUDIT_PATH)
    offer_id = str(offer_audit.get("offerId") or "").strip()
    if not offer_id:
        raise ValueError("offerId not found in real_offer_create_audit_v2.json")
    return {"offerId": offer_id}

def build_precheck(memory, runtime):
    return {
        "status": "OK",
        "decision": "real_offer_publish_precheck_completed",
        "action_name": "real_offer_publish",
        "offerId": runtime["offerId"],
        "known_failures": memory.get("known_failures", []),
        "working_paths": memory.get("working_paths", []),
        "cmd_traps": memory.get("cmd_traps", [])
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

    url = f"https://api.ebay.com/sell/inventory/v1/offer/{runtime['offerId']}/publish"
    response = requests.post(url, headers=headers, timeout=60)

    audit = {
        "status": "UNKNOWN",
        "decision": "real_offer_publish_sent",
        "offerId": runtime["offerId"],
        "http_status": response.status_code,
        "response_text": response.text[:4000]
    }

    try:
        response_json = response.json()
    except Exception:
        response_json = None

    if response_json is not None:
        audit["response_json"] = response_json

    if response.status_code in (200, 201):
        audit["status"] = "OK"
        audit["decision"] = "real_offer_published"
        write_json(AUDIT_PATH, audit)
        print("REAL_OFFER_PUBLISH_OK")
        print("decision = real_offer_published")
        print("offerId =", runtime["offerId"])
        print("http_status =", response.status_code)
        return

    audit["status"] = "ERROR"
    audit["decision"] = "real_offer_publish_failed"
    write_json(AUDIT_PATH, audit)
    print("REAL_OFFER_PUBLISH_FAILED")
    print("decision = real_offer_publish_failed")
    print("offerId =", runtime["offerId"])
    print("http_status =", response.status_code)

if __name__ == "__main__":
    main()
