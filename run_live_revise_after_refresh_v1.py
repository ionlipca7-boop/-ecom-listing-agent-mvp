import requests
from pathlib import Path

BASE = Path(__file__).resolve().parent
TOKEN = (BASE / "storage" / "secrets" / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
SKU = "USBCOTGAdapterUSB3TypeCtoUSB4q10p39"
OFFER_ID = "152921341011"

headers = {}
headers["Authorization"] = f"Bearer {TOKEN}"
headers["Content-Type"] = "application/json"
headers["Content-Language"] = "de-DE"

inv_get_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{SKU}"
off_get_url = f"https://api.ebay.com/sell/inventory/v1/offer/{OFFER_ID}"

inv_get = requests.get(inv_get_url, headers=headers, timeout=30)
off_get = requests.get(off_get_url, headers=headers, timeout=30)

inventory_put_status = "SKIPPED"
offer_put_status = "SKIPPED"

if inv_get.status_code == 200 and off_get.status_code == 200:
    inventory_payload = {
        "product": {
            "title": "USB-C auf USB-A OTG Adapter USB 3.0 6A Schnellladen Daten Konverter",
            "description": "USB-C auf USB-A OTG Adapter mit USB 3.0 und bis zu 6A Schnellladung. Geeignet fur Smartphones, Tablets, Laptops und viele USB-C Gerate. Ideal fur Datenubertragung und tagliche Nutzung zu Hause, im Buro oder unterwegs.",
            "aspects": {
                "Marke": ["Ohne Marke"],
                "Produktart": ["USB-C Adapter"],
                "Anschluss A": ["USB-C"],
                "Anschluss B": ["USB-A"],
                "Besonderheiten": ["OTG","USB 3.0","Schnellladen"],
                "Kompatibel mit": ["Samsung","MacBook","Android"]
            }
        },
        "availability": {"shipToLocationAvailability": {"quantity": 20}}
    }

    offer_payload = {
        "sku": SKU,
        "marketplaceId": "EBAY_DE",
        "format": "FIXED_PRICE",
        "availableQuantity": 20,
        "pricingSummary": {"price": {"value": "5.49", "currency": "EUR"}}
    }

    inv_put = requests.put(inv_get_url, headers=headers, json=inventory_payload, timeout=30)
    off_put = requests.put(off_get_url, headers=headers, json=offer_payload, timeout=30)
    inventory_put_status = inv_put.status_code
    offer_put_status = off_put.status_code

print("LIVE_REVISE_AFTER_REFRESH_V1_FINAL_AUDIT")
print("inventory_get_status =", inv_get.status_code)
print("offer_get_status =", off_get.status_code)
print("inventory_put_status =", inventory_put_status)
print("offer_put_status =", offer_put_status)
print("target_title = USB-C auf USB-A OTG Adapter USB 3.0 6A Schnellladen Daten Konverter")
print("target_price = 5.49")
