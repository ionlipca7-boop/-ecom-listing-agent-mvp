import json
import base64
import requests
from pathlib import Path

BASE = Path(__file__).resolve().parent
SECRETS = BASE / "storage" / "secrets"

def read_first(names):
    for name in names:
        path = SECRETS / name
        if path.exists():
            return path.read_text(encoding="utf-8").strip(), name
    return None, None

client_id, client_id_file = read_first(["ebay_client_id.txt","client_id.txt","ebay_app_id.txt"])
client_secret, client_secret_file = read_first(["ebay_client_secret.txt","client_secret.txt","ebay_cert_id.txt"])
refresh_token, refresh_token_file = read_first(["ebay_refresh_token.txt","refresh_token.txt"])

print("REFRESH_ACCESS_TOKEN_V1_FINAL_AUDIT")
print("client_id_file =", client_id_file)
print("client_secret_file =", client_secret_file)
print("refresh_token_file =", refresh_token_file)

if not client_id or not client_secret or not refresh_token:
    print("status = MISSING_SECRETS")
    print("http_status = NONE")
    print("token_saved = False")
    raise SystemExit(0)

basic = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
headers = {}
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Authorization"] = "Basic " + basic

data = {}
data["grant_type"] = "refresh_token"
data["refresh_token"] = refresh_token

res = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data, timeout=60)
print("http_status =", res.status_code)

try:
    payload = res.json()
except:
    payload = {"raw": res.text[:800]}

access_token = None
if isinstance(payload, dict):
    access_token = payload.get("access_token")

saved = False
if access_token:
    (SECRETS / "ebay_access_token.txt").write_text(access_token, encoding="utf-8")
    saved = True

print("token_saved =", saved)
print("has_access_token =", bool(access_token))
print("response_keys =", list(payload.keys())[:20] if isinstance(payload, dict) else "NO_JSON")
print("response_preview =", payload)
