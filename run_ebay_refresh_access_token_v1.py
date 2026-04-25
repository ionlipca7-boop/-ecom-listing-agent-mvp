import requests
import base64
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS = BASE_DIR / "storage" / "secrets"

def main():
    client_id = (SECRETS / "ebay_client_id.txt").read_text().strip()
    client_secret = (SECRETS / "ebay_client_secret.txt").read_text().strip()
    refresh_token = (SECRETS / "ebay_refresh_token.txt").read_text().strip()

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    r = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)
    print("REFRESH_STATUS =", r.status_code)
    print(r.text)

    if r.status_code == 200:
        token = r.json().get("access_token", "")
        (SECRETS / "ebay_access_token.txt").write_text(token)
        print("NEW_ACCESS_TOKEN_SAVED")

if __name__ == "__main__":
    main()
