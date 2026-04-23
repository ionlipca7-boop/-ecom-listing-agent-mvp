import requests
import json
from pathlib import Path

def read(p): return Path(p).read_text(encoding="utf-8").strip()

token = read(Path(r"storage\secrets\ebay_access_token.txt"))
sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"

url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
headers = {
  "Authorization": "Bearer " + token,
  "Content-Type": "application/json",
  "Content-Language": "de-DE"
}

# READ LIVE
r = requests.get(url, headers=headers)
data = r.json()

# BUILD CLEAN PRODUCT
product = {}
if "product" in data:
    p = data["product"]
    if "title" in p: product["title"] = p["title"]
    if "description" in p: product["description"] = p["description"]
    if "aspects" in p: product["aspects"] = p["aspects"]
    product["imageUrls"] = ["https://i.ebayimg.com/images/g/7MsAAeSw7kpp4-UD/s-l1600.webp"]

payload = {}

if "availability" in data: payload["availability"] = data["availability"]
if "condition" in data: payload["condition"] = data["condition"]
payload["product"] = product

if "packageWeightAndSize" in data: payload["packageWeightAndSize"] = data["packageWeightAndSize"]

r2 = requests.put(url, headers=headers, json=payload)

print("INVENTORY_CLEAN_FULL_UPDATE_WITH_IMAGES_V4")
print("read_status =", r.status_code)
print("update_status =", r2.status_code)
