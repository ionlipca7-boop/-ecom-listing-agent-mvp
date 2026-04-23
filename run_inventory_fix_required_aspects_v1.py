import json
import requests
from pathlib import Path

def read_text(p):
    return Path(p).read_text(encoding="utf-8").strip()

base = Path(".")
token = read_text(base / "storage" / "secrets" / "ebay_access_token.txt")
sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"

url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE",
    "Accept": "application/json"
}

r = requests.get(url, headers=headers, timeout=60)
data = r.json() if r.ok else {}

payload = {}
if data.get("availability") is not None: payload["availability"] = data["availability"]
if data.get("condition") is not None: payload["condition"] = data["condition"]
if data.get("conditionDescription") not in [None, ""]: payload["conditionDescription"] = data["conditionDescription"]
if data.get("conditionDescriptors") not in [None, []]: payload["conditionDescriptors"] = data["conditionDescriptors"]
if data.get("packageWeightAndSize") is not None: payload["packageWeightAndSize"] = data["packageWeightAndSize"]

live_product = data.get("product", {}) if isinstance(data.get("product", {}), dict) else {}
product = {}
if live_product.get("title"): product["title"] = live_product["title"]
if live_product.get("description"): product["description"] = live_product["description"]
if live_product.get("subtitle"): product["subtitle"] = live_product["subtitle"]
if live_product.get("brand"): product["brand"] = live_product["brand"]
if live_product.get("mpn"): product["mpn"] = live_product["mpn"]
if live_product.get("ean"): product["ean"] = live_product["ean"]
if live_product.get("upc"): product["upc"] = live_product["upc"]
if live_product.get("isbn"): product["isbn"] = live_product["isbn"]
if live_product.get("epid"): product["epid"] = live_product["epid"]

aspects = live_product.get("aspects", {}) if isinstance(live_product.get("aspects", {}), dict) else {}
if not aspects.get("Marke"): aspects["Marke"] = ["Markenlos"]
if not aspects.get("Produktart"): aspects["Produktart"] = ["Adapter"]
if not aspects.get("Herstellernummer"): aspects["Herstellernummer"] = ["Nicht zutreffend"]
product["aspects"] = aspects
product["imageUrls"] = ["https://i.ebayimg.com/images/g/7MsAAeSw7kpp4-UD/s-l1600.webp"]
payload["product"] = product

r2 = requests.put(url, headers=headers, json=payload, timeout=60)

try:
    err = r2.json()
except Exception:
    err = None

out = {
    "status": "OK" if r2.status_code in [200,204] else "FAILED",
    "decision": "inventory_fix_required_aspects_v1_executed",
    "sku": sku,
    "read_status": r.status_code,
    "update_status": r2.status_code,
    "marke_present": "Marke" in aspects,
    "produktart_present": "Produktart" in aspects,
    "herstellernummer_present": "Herstellernummer" in aspects,
    "images_sent": len(product.get("imageUrls", [])),
    "response_text": r2.text[:2000],
    "response_json": err,
    "next_step": "rebuild_multi_image_inventory_update_v1" if r2.status_code in [200,204] else "inspect_next_missing_required_aspect_v1"
}
Path(r"storage\exports\inventory_fix_required_aspects_v1_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("INVENTORY_FIX_REQUIRED_ASPECTS_V1_FINAL_AUDIT")
print("status =", out["status"])
print("decision =", out["decision"])
print("read_status =", out["read_status"])
print("update_status =", out["update_status"])
print("marke_present =", out["marke_present"])
print("produktart_present =", out["produktart_present"])
print("herstellernummer_present =", out["herstellernummer_present"])
print("images_sent =", out["images_sent"])
print("next_step =", out["next_step"])
