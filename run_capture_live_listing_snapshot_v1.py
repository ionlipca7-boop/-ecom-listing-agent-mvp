import json
import requests
import xml.etree.ElementTree as ET
from pathlib import Path

def read_text(p):
    return Path(p).read_text(encoding="utf-8").strip()

base = Path(".")
token = read_text(base / "storage" / "secrets" / "ebay_access_token.txt")
sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
offer_id = "153365657011"
item_id = "318166440509"

inv_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
offer_url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
rest_headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Content-Language": "de-DE"
}

r_inv = requests.get(inv_url, headers=rest_headers, timeout=60)
inv = r_inv.json() if r_inv.ok else {}
r_offer = requests.get(offer_url, headers=rest_headers, timeout=60)
offer = r_offer.json() if r_offer.ok else {}

xml_body = """<?xml version="1.0" encoding="utf-8"?^><GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents"^><RequesterCredentials^><eBayAuthToken^>""" + token + """^</eBayAuthToken^></RequesterCredentials^><ItemID^>""" + item_id + """^</ItemID^><DetailLevel^>ReturnAll^</DetailLevel^><IncludeItemSpecifics^>true^</IncludeItemSpecifics^></GetItemRequest^>"""
xml_headers = {
    "Content-Type": "text/xml",
    "X-EBAY-API-CALL-NAME": "GetItem",
    "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
    "X-EBAY-API-SITEID": "77"
}
r_item = requests.post("https://api.ebay.com/ws/api.dll", headers=xml_headers, data=xml_body.encode("utf-8"), timeout=60)

ack = ""
title = ""
current_price = ""
picture_urls = []
try:
    root = ET.fromstring(r_item.text)
    ns = {"e": "urn:ebay:apis:eBLBaseComponents"}
    ack = root.findtext(".//e:Ack", default="", namespaces=ns)
    title = root.findtext(".//e:Title", default="", namespaces=ns)
    current_price = root.findtext(".//e:CurrentPrice", default="", namespaces=ns)
    picture_urls = [n.text for n in root.findall(".//e:PictureURL", ns) if n.text]
except Exception:
    pass

out = {
  "status": "OK",
  "decision": "live_listing_snapshot_v1_captured",
  "sku": sku,
  "offer_id": offer_id,
  "item_id": item_id,
  "inventory_http_status": r_inv.status_code,
  "offer_http_status": r_offer.status_code,
  "trading_http_status": r_item.status_code,
  "trading_ack": ack,
  "trading_title": title,
  "trading_price": current_price,
  "trading_picture_count": len(picture_urls),
  "inventory_picture_count": len((inv.get("product", {}) if isinstance(inv.get("product", {}), dict) else {}).get("imageUrls", [])),
  "offer_picture_count": len(offer.get("imageUrls", [])),
  "trading_picture_urls": picture_urls,
  "inventory_payload": inv,
  "offer_payload": offer,
  "next_step": "archive_working_listing_baseline_v1"
}

Path(r"storage\exports\live_listing_snapshot_v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("LIVE_LISTING_SNAPSHOT_V1_FINAL_AUDIT")
print("status =", out["status"])
print("decision =", out["decision"])
print("inventory_http_status =", out["inventory_http_status"])
print("offer_http_status =", out["offer_http_status"])
print("trading_http_status =", out["trading_http_status"])
print("trading_ack =", out["trading_ack"])
print("trading_price =", out["trading_price"])
print("trading_picture_count =", out["trading_picture_count"])
print("inventory_picture_count =", out["inventory_picture_count"])
print("offer_picture_count =", out["offer_picture_count"])
print("next_step =", out["next_step"])
