import base64
import json
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

def read_text(name: str) -> str:
    return (SECRETS_DIR / name).read_text(encoding="utf-8").strip()

def main() -> None:
    client_id = read_text("ebay_client_id.txt")
    client_secret = read_text("ebay_client_secret.txt")
    redirect_uri = read_text("ebay_redirect_uri.txt")

    print("CLIENT_ID_PREFIX =", client_id[:12])
    print("REDIRECT_URI =", redirect_uri)
    print("PASTE_FULL_REDIRECT_URL:")
    redirect_full_url = input().strip()

    parsed = urllib.parse.urlparse(redirect_full_url)
    params = urllib.parse.parse_qs(parsed.query)
    code = params.get("code", [""])[0]

    if not code:
        raise SystemExit("ERROR: code not found in redirect URL")

    basic_raw = f"{client_id}:{client_secret}".encode("utf-8")
    basic_b64 = base64.b64encode(basic_raw).decode("ascii")

    payload = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }).encode("utf-8")

    request = urllib.request.Request(TOKEN_URL, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {basic_b64}"}, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            response_text = response.read().decode("utf-8")
            status_code = response.getcode()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        audit = {"status": "FAILED", "http_status": e.code, "body": body}
        (EXPORTS_DIR / "ebay_oauth_token_exchange_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("TOKEN_EXCHANGE_FAILED")
        print("status_code =", e.code)
        print(body)
        raise SystemExit(1)

    data = json.loads(response_text)
    access_token = data.get("access_token", "").strip()
    refresh_token = data.get("refresh_token", "").strip()

    if not access_token:
        raise SystemExit("ERROR: access_token missing in response")

    (SECRETS_DIR / "ebay_access_token.txt").write_text(access_token, encoding="utf-8")
    if refresh_token:
        (SECRETS_DIR / "ebay_refresh_token.txt").write_text(refresh_token, encoding="utf-8")

    audit = {"status": "OK", "http_status": status_code, "access_token_saved": bool(access_token), "refresh_token_saved": bool(refresh_token), "expires_in": data.get("expires_in"), "refresh_token_expires_in": data.get("refresh_token_expires_in"), "token_type": data.get("token_type")}
    (EXPORTS_DIR / "ebay_oauth_token_exchange_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print("TOKEN_EXCHANGE_OK")
    print("http_status =", status_code)
    print("access_token_saved =", bool(access_token))
    print("refresh_token_saved =", bool(refresh_token))
    print("expires_in =", data.get("expires_in"))
    print("refresh_token_expires_in =", data.get("refresh_token_expires_in"))

if __name__ == "__main__":
    main()
