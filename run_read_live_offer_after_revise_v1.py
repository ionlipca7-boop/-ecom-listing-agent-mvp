import json
import requests
from pathlib import Path

def read(p): return Path(p).read_text(encoding="utf-8").strip()

base = Path(".")
token = read(base / "storage" / "secrets" / "ebay_access_token.txt")
offer_id = "153365657011"

url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
headers = {
    "Authorization": "Bearer " + token,
    "Content-Language": "de-DE",
    "Accept": "application/json"
}

r = requests.get(url, headers=headers)
data = r.json() if r.ok else {}

images = data.get("imageUrls", [])
price = None
try:
    price = data["pricingSummary"]["price"]["value"]
except:
    pass

print("READ_LIVE_OFFER_AFTER_REVISE_V1")
print("http_status =", r.status_code)
print("price =", price)
print("image_count =", len(images))
print("has_policies =", bool(data.get("listingPolicies")))
print("has_location =", bool(data.get("merchantLocationKey")))
print("has_description =", bool(data.get("listingDescription")))
