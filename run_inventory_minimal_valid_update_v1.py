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
  "availability": {
    "shipToLocationAvailability": {
      "quantity": 10
    }
  },
  "condition": "NEW",
  "product": {
    "title": "USB-C OTG Adapter 120W Typ C auf USB A Schnellladen",
    "description": "USB-C OTG Adapter fur Datenubertragung und Schnellladen. Kompatibel mit Samsung, MacBook und weiteren Geraten.",
    "imageUrls": [
      "https://i.ebayimg.com/images/g/7MsAAeSw7kpp4-UD/s-l1600.webp"
    ]
  }
}

r = requests.put(url, headers=headers, json=payload)

print("INVENTORY_MINIMAL_VALID_UPDATE_V1")
print("http_status =", r.status_code)
print("response =", r.text[:300])
