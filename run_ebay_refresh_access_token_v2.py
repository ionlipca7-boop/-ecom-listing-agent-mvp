import requests
import base64
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS = BASE_DIR / "storage" / "secrets"
EXPORTS = BASE_DIR / "storage" / "exports"
OUTPUT_PATH = EXPORTS / "ebay_refresh_access_token_audit_v2.json"

SCOPES = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment https://api.ebay.com/oauth/api_scope/sell.analytics.readonly"

def main():
    client_id = (SECRETS / "ebay_client_id.txt").read_text(encoding="utf-8").strip()
    client_secret = (SECRETS / "ebay_client_secret.txt").read_text(encoding="utf-8").strip()
    refresh_token = (SECRETS / "ebay_refresh_token.txt").read_text(encoding="utf-8").strip()
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": SCOPES
    }
    r = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data, timeout=60)
    try:
        payload = r.json()
    except Exception:
        payload = {"raw_text": r.text[:2000]}
    token = payload.get("access_token", "") if isinstance(payload, dict) else ""
    if token:
        (SECRETS / "ebay_access_token.txt").write_text(token, encoding="utf-8")
    audit = {
        "status": "OK" if r.status_code == 200 and bool(token) else "FAILED",
        "http_status": r.status_code,
        "access_token_saved": bool(token),
        "access_token_length": len(token),
        "scope_used": SCOPES,
        "response": payload
    }
    OUTPUT_PATH.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print("EBAY_REFRESH_ACCESS_TOKEN_V2")
    print("http_status =", r.status_code)
    print("access_token_saved =", bool(token))
    print("access_token_length =", len(token))

if __name__ == "__main__":
    main()
