import base64
import json
import urllib.parse
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REDIRECT_RESULT_URL_PATH = SECRETS_DIR / "ebay_redirect_result_url.txt"
ACCESS_TOKEN_PATH = SECRETS_DIR / "ebay_access_token.txt"
REFRESH_TOKEN_PATH = SECRETS_DIR / "ebay_refresh_token.txt"
OUTPUT_FILE = EXPORTS_DIR / "ebay_exchange_code_audit_v1.json"
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    client_id = read_text(SECRETS_DIR / "ebay_client_id.txt")
    client_secret = read_text(SECRETS_DIR / "ebay_client_secret.txt")
    redirect_uri = read_text(SECRETS_DIR / "ebay_redirect_uri.txt")
    redirect_result_url = read_text(REDIRECT_RESULT_URL_PATH)
    parsed = urllib.parse.urlparse(redirect_result_url)
    qs = urllib.parse.parse_qs(parsed.query)
    code = qs.get("code", [""])[0]
    creds = client_id + ":" + client_secret
    basic = base64.b64encode(creds.encode("utf-8")).decode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + basic}
    data = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}
    response = requests.post(TOKEN_URL, headers=headers, data=data, timeout=60)
    try:
        response_json = response.json()
    except Exception:
        response_json = {"raw_text": response.text}
    access_token = response_json.get("access_token", "")
    refresh_token = response_json.get("refresh_token", "")
    if access_token:
        ACCESS_TOKEN_PATH.write_text(access_token.strip(), encoding="utf-8")
    if refresh_token:
        REFRESH_TOKEN_PATH.write_text(refresh_token.strip(), encoding="utf-8")
    result = {"status": "OK" if response.status_code == 200 and bool(access_token) else "FAILED", "http_status": response.status_code, "has_access_token": bool(access_token), "access_token_length": len(access_token), "has_refresh_token": bool(refresh_token), "refresh_token_length": len(refresh_token), "response_json": response_json}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("EXCHANGE_CODE_V1_DONE")
    print("http_status =", response.status_code)
    print("has_access_token =", bool(access_token))
    print("access_token_length =", len(access_token))

if __name__ == "__main__":
    main()
