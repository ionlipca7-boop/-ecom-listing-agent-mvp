import json
import secrets
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
CLIENT_ID_PATH = SECRETS_DIR / "ebay_client_id.txt"
RU_NAME_PATH = SECRETS_DIR / "ebay_ru_name.txt"
STATE_PATH = SECRETS_DIR / "ebay_oauth_state_v1.txt"
OUTPUT_PATH = EXPORTS_DIR / "ebay_oauth_consent_url_v1.json"

SCOPES = [
    "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
    "https://api.ebay.com/oauth/api_scope/sell.account",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
    "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly"
]

def main():
    client_id = CLIENT_ID_PATH.read_text(encoding="utf-8").strip()
    ru_name = RU_NAME_PATH.read_text(encoding="utf-8").strip()
    state = secrets.token_urlsafe(24)
    STATE_PATH.write_text(state, encoding="utf-8")
    params = {
        "client_id": client_id,
        "redirect_uri": ru_name,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": state
    }
    consent_url = "https://auth.ebay.com/oauth2/authorize?" + urllib.parse.urlencode(params)
    result = {
        "status": "OK",
        "decision": "consent_url_ready",
        "redirect_uri_name": ru_name,
        "scopes": SCOPES,
        "state_saved": True,
        "consent_url": consent_url
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("EBAY_OAUTH_CONSENT_URL_V1")
    print("redirect_uri_name =", ru_name)
    print("state_saved =", True)
    print("consent_url =", consent_url)

if __name__ == "__main__":
    main()
