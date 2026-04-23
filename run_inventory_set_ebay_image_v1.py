import requests
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

payload = {
  "product": {
    "imageUrls": [
      "https://i.ebayimg.com/images/g/7MsAAeSw7kpp4-UD/s-l1600.webp"
    ]
  }
}

r = requests.put(url, headers=headers, json=payload)

print("INVENTORY_SET_EBAY_IMAGE_V1")
print("http_status =", r.status_code)
print("image_used = ebay_cdn")
