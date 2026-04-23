import secrets
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def read_secret(name):
    return (SECRETS_DIR / name).read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    client_id = read_secret("ebay_client_id.txt")
    redirect_uri = read_secret("ebay_redirect_uri.txt")
    state = secrets.token_hex(16)
    scopes = [
        "https://api.ebay.com/oauth/api_scope/sell.account",
        "https://api.ebay.com/oauth/api_scope/sell.inventory"
    ]
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scopes),
        "state": state
    }
    url = "https://auth.ebay.com/oauth2/authorize?" + urllib.parse.urlencode(params)
    (EXPORTS_DIR / "ebay_oauth_consent_url_v2.txt").write_text(url, encoding="utf-8")
    (EXPORTS_DIR / "ebay_oauth_state_v2.txt").write_text(state, encoding="utf-8")
    print("EBAY_OAUTH_CONSENT_URL_V2_READY")
    print("state =", state)
    print("consent_url_file = storage\\exports\\ebay_oauth_consent_url_v2.txt")
    print("scope_count =", len(scopes))
    print("scope_1 =", scopes[0])
    print("scope_2 =", scopes[1])

if __name__ == "__main__":
    main()
