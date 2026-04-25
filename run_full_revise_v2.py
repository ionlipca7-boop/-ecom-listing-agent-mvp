import requests
from pathlib import Path
BASE = Path(__file__).resolve().parent
TOKEN = (BASE / "storage" / "secrets" / "ebay_access_token.txt").read_text().strip()
SKU = "USBCOTGAdapterUSB3TypeCtoUSB4q10p39"
OFFER_ID = "152921341011"
headers = {
"Authorization": f"Bearer {TOKEN}",
"Content-Type": "application/json",
"Content-Language": "de-DE"
}
inventory_payload = {
"product": {
"title": "USB-C auf USB-A OTG Adapter 3.0 6A Schnellladen Daten Samsung MacBook",
"description": "USB-C auf USB-A OTG Adapter mit USB 3.0 und 6A Schnellladung. Perfekt fur Smartphones, Tablets und Laptops.",
"aspects": {
"Marke": ["Ohne Marke"],
"Produktart": ["USB-C Adapter"],
"Anschluss A": ["USB-C"],
"Anschluss B": ["USB-A"],
"Besonderheiten": ["OTG","Schnellladen","USB 3.0"],
"Kompatibel mit": ["Samsung","MacBook","Android"]
}
},
"availability": {"shipToLocationAvailability": {"quantity": 20}}
}
requests.put(f"https://api.ebay.com/sell/inventory/v1/inventory_item/{SKU}",headers=headers,json=inventory_payload)
offer_payload = {
"sku": SKU,
"marketplaceId": "EBAY_DE",
"format": "FIXED_PRICE",
"availableQuantity": 20,
"pricingSummary": {"price": {"value": "5.49","currency": "EUR"}}
}
requests.put(f"https://api.ebay.com/sell/inventory/v1/offer/{OFFER_ID}",headers=headers,json=offer_payload)
print("FULL_REVISE_DONE")
