import base64
import json
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REDIRECT_URL_FILE = EXPORTS_DIR / "ebay_oauth_redirect_url_v2.txt"

def read_secret(name):
    return (SECRETS_DIR / name).read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    client_id = read_secret("ebay_client_id.txt")
    client_secret = read_secret("ebay_client_secret.txt")
    redirect_uri = read_secret("ebay_redirect_uri.txt")
    redirect_url = REDIRECT_URL_FILE.read_text(encoding="utf-8").strip()
    parsed = urllib.parse.urlparse(redirect_url)
    qs = urllib.parse.parse_qs(parsed.query)
    code = qs.get("code", [""])[0]
    if not code:
        raise SystemExit("NO_CODE_IN_REDIRECT_URL")
    basic = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
    form = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.ebay.com/identity/v1/oauth2/token",
        data=form,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + basic
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.getcode()
            raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        access_token = data.get("access_token", "")
        refresh_token = data.get("refresh_token", "")
        if access_token:
            (SECRETS_DIR / "ebay_access_token.txt").write_text(access_token, encoding="utf-8")
        if refresh_token:
            (SECRETS_DIR / "ebay_refresh_token.txt").write_text(refresh_token, encoding="utf-8")
        (EXPORTS_DIR / "ebay_oauth_token_exchange_v3.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        audit = {
            "status": "OK",
            "http_status": status_code,
            "access_token_saved": bool(access_token),
            "refresh_token_saved": bool(refresh_token),
            "token_type": data.get("token_type"),
            "expires_in": data.get("expires_in"),
            "refresh_token_expires_in": data.get("refresh_token_expires_in"),
            "scope": data.get("scope")
        }
        (EXPORTS_DIR / "ebay_oauth_token_exchange_audit_v3.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("TOKEN_EXCHANGE_V3_OK")
        print("http_status =", status_code)
        print("access_token_saved =", bool(access_token))
        print("refresh_token_saved =", bool(refresh_token))
        print("expires_in =", data.get("expires_in"))
        print("scope =", data.get("scope"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        audit = {"status": "FAILED", "http_status": e.code, "body": raw}
        (EXPORTS_DIR / "ebay_oauth_token_exchange_audit_v3.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("TOKEN_EXCHANGE_V3_FAILED")
        print("http_status =", e.code)
        print(raw)

if __name__ == "__main__":
    main()
