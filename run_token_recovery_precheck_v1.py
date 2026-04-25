import base64
import json
from datetime import UTC, datetime
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_v1.json"
AUDIT_FILE = EXPORTS_DIR / "token_recovery_precheck_v1.json"

def read_text_if_exists(path):
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""

def pick_first_existing(candidates):
    for rel in candidates:
        path = SECRETS_DIR / rel
        if path.exists():
            return path
    return None

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    memory = {}
    if MEMORY_FILE.exists():
        memory = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    access_path = pick_first_existing(["ebay_access_token.txt", "ebay_user_token.txt"])
    refresh_path = pick_first_existing(["ebay_refresh_token.txt"])
    client_id_path = pick_first_existing(["ebay_client_id.txt", "client_id.txt"])
    client_secret_path = pick_first_existing(["ebay_client_secret.txt", "client_secret.txt"])
    access_token = read_text_if_exists(access_path) if access_path else ""
    refresh_token = read_text_if_exists(refresh_path) if refresh_path else ""
    client_id = read_text_if_exists(client_id_path) if client_id_path else ""
    client_secret = read_text_if_exists(client_secret_path) if client_secret_path else ""
    result = {
        "status": "OK",
        "decision": "token_precheck_completed",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "memory_next_target": memory.get("next_target", {}).get("product_key"),
        "access_token_file": str(access_path.relative_to(BASE_DIR)) if access_path else None,
        "refresh_token_file": str(refresh_path.relative_to(BASE_DIR)) if refresh_path else None,
        "client_id_file": str(client_id_path.relative_to(BASE_DIR)) if client_id_path else None,
        "client_secret_file": str(client_secret_path.relative_to(BASE_DIR)) if client_secret_path else None,
        "access_token_length": len(access_token),
        "refresh_token_length": len(refresh_token),
        "client_id_present": bool(client_id),
        "client_secret_present": bool(client_secret),
        "refresh_attempted": False,
        "refresh_http_status": None,
        "refresh_ok": False
    }
    if refresh_token and client_id and client_secret:
        auth = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
        headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "refresh_token", "refresh_token": refresh_token, "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment"}
        result["refresh_attempted"] = True
        try:
            response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data, timeout=60)
            result["refresh_http_status"] = response.status_code
            raw = response.json()
            result["refresh_response_keys"] = list(raw.keys())[:10]
            new_access_token = raw.get("access_token", "")
            if response.status_code == 200 and new_access_token:
                out_path = SECRETS_DIR / "ebay_access_token.txt"
                out_path.write_text(new_access_token.strip(), encoding="utf-8")
                result["refresh_ok"] = True
                result["decision"] = "access_token_refreshed" 
                result["new_access_token_file"] = str(out_path.relative_to(BASE_DIR))
                result["new_access_token_length"] = len(new_access_token.strip())
            else:
                result["status"] = "ERROR"
                result["decision"] = "access_token_refresh_failed"
                result["refresh_error"] = raw
        except Exception as e:
            result["status"] = "ERROR"
            result["decision"] = "refresh_exception"
            result["exception"] = str(e)
    AUDIT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TOKEN_RECOVERY_PRECHECK_DONE")
    print("status =", result["status"])
    print("decision =", result["decision"])
    print("access_token_length =", result["access_token_length"])
    print("refresh_token_length =", result["refresh_token_length"])
    print("refresh_attempted =", result["refresh_attempted"])
    print("refresh_ok =", result["refresh_ok"])
    print("refresh_http_status =", result["refresh_http_status"])

if __name__ == "__main__":
    main()
