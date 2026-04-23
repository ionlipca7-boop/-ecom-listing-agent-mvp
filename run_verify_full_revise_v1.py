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

inv_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{SKU}"
off_url = f"https://api.ebay.com/sell/inventory/v1/offer/{OFFER_ID}"

inv_res = requests.get(inv_url, headers=headers, timeout=30)
off_res = requests.get(off_url, headers=headers, timeout=30)

try:
    inv_json = inv_res.json()
except:
    inv_json = {"raw": inv_res.text[:500]}

try:
    off_json = off_res.json()
except:
    off_json = {"raw": off_res.text[:500]}

inv_title = None
if isinstance(inv_json, dict):
    product = inv_json.get("product", {})
    if isinstance(product, dict):
        inv_title = product.get("title")

off_price = None
if isinstance(off_json, dict):
    pricing = off_json.get("pricingSummary", {})
    if isinstance(pricing, dict):
        price = pricing.get("price", {})
        if isinstance(price, dict):
            off_price = price.get("value")

print("FULL_REVISE_VERIFY_V1_FINAL_AUDIT")
print("inventory_http_status =", inv_res.status_code)
print("offer_http_status =", off_res.status_code)
print("inventory_title =", inv_title)
print("offer_price =", off_price)
print("inventory_top_keys =", list(inv_json.keys())[:12] if isinstance(inv_json, dict) else "NO_JSON")
print("offer_top_keys =", list(off_json.keys())[:12] if isinstance(off_json, dict) else "NO_JSON")
print("inventory_preview =", inv_json)
print("offer_preview =", off_json)
