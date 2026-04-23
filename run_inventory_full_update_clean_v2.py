import json
import requests
from pathlib import Path

def read(p): return Path(p).read_text(encoding="utf-8").strip()
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))

base = Path(".")
token = read(base / "storage" / "secrets" / "ebay_access_token.txt")
archive = load(base / "storage" / "memory" / "archive" / "photo_source_archive_v2.json")
sku = archive["sku"]
images = archive["image_urls"]

url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE"
}

r = requests.get(url, headers=headers)
data = r.json()

payload = {
  "availability": data.get("availability"),
  "condition": data.get("condition"),
  "product": {
      "title": data.get("product", {}).get("title"),
      "description": data.get("product", {}).get("description"),
      "aspects": data.get("product", {}).get("aspects"),
      "imageUrls": images
  }
}

r2 = requests.put(url, headers=headers, json=payload)

print("INVENTORY_FULL_UPDATE_CLEAN_V2")
print("read_status =", r.status_code)
print("update_status =", r2.status_code)
print("images_sent =", len(images))
