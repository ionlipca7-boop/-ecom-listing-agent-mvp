import json
import requests
from pathlib import Path

def read(p): return Path(p).read_text(encoding="utf-8").strip()
def write(p, v): Path(p).write_text(v, encoding="utf-8")
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

base = Path(".")
payload_path = base / "storage" / "exports" / "safe_full_offer_payload_v2.json"
access_path = base / "storage" / "secrets" / "ebay_access_token.txt"
refresh_path = base / "storage" / "secrets" / "ebay_refresh_token.txt"

client_id = read(base / "storage" / "secrets" / "ebay_client_id.txt")
client_secret = read(base / "storage" / "secrets" / "ebay_client_secret.txt")
refresh_token = read(refresh_path)

token_resp = requests.post("https://api.ebay.com/identity/v1/oauth2/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "https://api.ebay.com/oauth/api_scope/sell.inventory"
    },
    auth=(client_id, client_secret)
)

token_data = token_resp.json()
access_token = token_data.get("access_token")
write(access_path, access_token)

data = load(payload_path)
payload = data["payload"]
payload["pricingSummary"]["price"]["value"] = "4.05"
offer_id = data["offer_id"]

url = "https://api.ebay.com/sell/inventory/v1/offer/" + str(offer_id)
headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE"
}

r = requests.put(url, headers=headers, json=payload)

print("REVISE_V2_DONE")
print("token_status =", token_resp.status_code)
print("http_status =", r.status_code)
print("price_sent = 4.05")
