import urllib.parse
from pathlib import Path
BASE_DIR = Path(__file__).parent
SECRETS = BASE_DIR / "storage" / "secrets"
CLIENT_ID = (SECRETS / "ebay_client_id.txt").read_text().strip()
REDIRECT_URI = (SECRETS / "ebay_redirect_uri.txt").read_text().strip()
SCOPES = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory https://api.ebay.com/oauth/api_scope/sell.account https://api.ebay.com/oauth/api_scope/sell.fulfillment"
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPES
}
url = "https://auth.ebay.com/oauth2/authorize?" + urllib.parse.urlencode(params)
print("CONSENT_URL:")
print(url)
