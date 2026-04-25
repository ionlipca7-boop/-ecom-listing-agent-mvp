import json
import requests
from pathlib import Path

def read_text(p):
    return Path(p).read_text(encoding="utf-8").strip()

def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))

base = Path(".")
token = read_text(base / "storage" / "secrets" / "ebay_access_token.txt")
sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
src = load_json(base / "storage" / "exports" / "eps_upload_queue_v1_result.json")

image_urls = ["https://i.ebayimg.com/images/g/7MsAAeSw7kpp4-UD/s-l1600.webp"]
for row in src.get("eps_successes", []):
    u = row.get("eps_url")
    if u:
        image_urls.append(u)

url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE",
    "Accept": "application/json"
}
read_headers = {
    "Authorization": "Bearer " + token,
    "Content-Language": "de-DE",
    "Accept": "application/json"
}

r1 = requests.get(url, headers=read_headers, timeout=60)
live = r1.json() if r1.ok else {}

payload = {}
if live.get("availability") is not None: payload["availability"] = live["availability"]
if live.get("condition") is not None: payload["condition"] = live["condition"]
if live.get("conditionDescription") not in [None, ""]: payload["conditionDescription"] = live["conditionDescription"]
if live.get("conditionDescriptors") not in [None, []]: payload["conditionDescriptors"] = live["conditionDescriptors"]
if live.get("packageWeightAndSize") is not None: payload["packageWeightAndSize"] = live["packageWeightAndSize"]

lp = live.get("product", {}) if isinstance(live.get("product", {}), dict) else {}
product = {}
if lp.get("title"): product["title"] = lp["title"]
if lp.get("description"): product["description"] = lp["description"]
if lp.get("subtitle"): product["subtitle"] = lp["subtitle"]
if lp.get("brand"): product["brand"] = lp["brand"]
if lp.get("mpn"): product["mpn"] = lp["mpn"]
if lp.get("ean"): product["ean"] = lp["ean"]
if lp.get("upc"): product["upc"] = lp["upc"]
if lp.get("isbn"): product["isbn"] = lp["isbn"]
if lp.get("epid"): product["epid"] = lp["epid"]
product["aspects"] = lp.get("aspects", {}) if isinstance(lp.get("aspects", {}), dict) else {}
product["imageUrls"] = image_urls
payload["product"] = product

r2 = requests.put(url, headers=headers, json=payload, timeout=60)
r3 = requests.get(url, headers=read_headers, timeout=60)
live2 = r3.json() if r3.ok else {}
live_image_count = len((live2.get("product", {}) if isinstance(live2.get("product", {}), dict) else {}).get("imageUrls", []))

out = {
  "status": "OK" if (r1.status_code == 200 and r2.status_code in [200,204] and r3.status_code == 200) else "FAILED",
  "decision": "multi_image_inventory_update_from_eps_v1_executed",
  "sku": sku,
  "read_before_status": r1.status_code,
  "update_status": r2.status_code,
  "read_after_status": r3.status_code,
  "images_sent": len(image_urls),
  "live_image_count": live_image_count,
  "next_step": "read_live_offer_after_multi_image_inventory_update_v1" if (r2.status_code in [200,204]) else "inspect_multi_image_inventory_error_v1"
}
Path(r"storage\exports\multi_image_inventory_update_from_eps_v1_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("MULTI_IMAGE_INVENTORY_UPDATE_FROM_EPS_V1_FINAL_AUDIT")
print("status =", out["status"])
print("decision =", out["decision"])
print("sku =", out["sku"])
print("read_before_status =", out["read_before_status"])
print("update_status =", out["update_status"])
print("read_after_status =", out["read_after_status"])
print("images_sent =", out["images_sent"])
print("live_image_count =", out["live_image_count"])
print("next_step =", out["next_step"])
