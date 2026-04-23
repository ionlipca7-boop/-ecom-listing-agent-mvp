import requests
import json
from pathlib import Path

def read(p): return Path(p).read_text(encoding="utf-8").strip()
def read_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))

token = read(Path(r"storage\secrets\ebay_access_token.txt"))
sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"

url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
headers = {
  "Authorization": "Bearer " + token,
  "Content-Type": "application/json",
  "Content-Language": "de-DE"
}

# STEP 1: READ LIVE
r = requests.get(url, headers=headers)
data = r.json()
product = data.get("product", {})

# STEP 2: INJECT IMAGE
product["imageUrls"] = [
  "https://i.ebayimg.com/images/g/7MsAAeSw7kpp4-UD/s-l1600.webp"
]

# STEP 3: FULL PAYLOAD
payload = data
payload["product"] = product

# STEP 4: UPDATE
r2 = requests.put(url, headers=headers, json=payload)

print("INVENTORY_FULL_UPDATE_WITH_IMAGES_V3")
print("read_status =", r.status_code)
print("update_status =", r2.status_code)
