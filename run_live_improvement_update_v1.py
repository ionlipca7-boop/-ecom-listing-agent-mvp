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
brief = load_json(base / "storage" / "exports" / "improvement_brief_v1.json")
snapshot = load_json(base / "storage" / "exports" / "live_listing_snapshot_v1.json")
sku = brief["sku"]
offer_id = brief["offer_id"]

inv_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
offer_url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
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

image_urls = [row["url"] for row in brief.get("photo_order_plan", []) if row.get("url")]
live_inv = snapshot.get("inventory_payload", {})
live_offer = snapshot.get("offer_payload", {})

inv_payload = {}
if live_inv.get("availability") is not None: inv_payload["availability"] = live_inv["availability"]
if live_inv.get("condition") is not None: inv_payload["condition"] = live_inv["condition"]
if live_inv.get("packageWeightAndSize") is not None: inv_payload["packageWeightAndSize"] = live_inv["packageWeightAndSize"]
inv_payload["product"] = {
    "title": brief["target_title"],
    "description": "USB-C OTG Adapter fuer Laden und Datenuebertragung. Geeignet fuer Smartphone, Tablet, Laptop und Zubehoer.",
    "aspects": live_inv.get("product", {}).get("aspects", {}),
    "imageUrls": image_urls
}

r_inv_put = requests.put(inv_url, headers=headers, json=inv_payload, timeout=60)
r_inv_get = requests.get(inv_url, headers=read_headers, timeout=60)
inv_after = r_inv_get.json() if r_inv_get.ok else {}

offer_payload = live_offer.copy()
offer_payload["sku"] = sku
offer_payload["listingDescription"] = brief["target_description_html"].replace("^","")
if "pricingSummary" not in offer_payload: offer_payload["pricingSummary"] = {"price": {"value": brief["baseline_price"], "currency": "EUR"}}
if "price" not in offer_payload["pricingSummary"]: offer_payload["pricingSummary"]["price"] = {"value": brief["baseline_price"], "currency": "EUR"}
offer_payload["pricingSummary"]["price"]["value"] = brief["baseline_price"]
if not offer_payload.get("availableQuantity"): offer_payload["availableQuantity"] = live_inv.get("availability", {}).get("shipToLocationAvailability", {}).get("quantity", 10)

r_offer_put = requests.put(offer_url, headers=headers, json=offer_payload, timeout=60)
r_offer_get = requests.get(offer_url, headers=read_headers, timeout=60)
offer_after = r_offer_get.json() if r_offer_get.ok else {}

out = {
  "status": "OK" if (r_inv_put.status_code in [200,204] and r_offer_put.status_code in [200,204] and r_inv_get.status_code == 200 and r_offer_get.status_code == 200) else "FAILED",
  "decision": "live_improvement_update_v1_executed",
  "sku": sku,
  "offer_id": offer_id,
  "inventory_put_status": r_inv_put.status_code,
  "inventory_read_status": r_inv_get.status_code,
  "offer_put_status": r_offer_put.status_code,
  "offer_read_status": r_offer_get.status_code,
  "inventory_title_after": inv_after.get("product", {}).get("title", ""),
  "inventory_image_count_after": len(inv_after.get("product", {}).get("imageUrls", [])),
  "offer_price_after": offer_after.get("pricingSummary", {}).get("price", {}).get("value", ""),
  "offer_has_description_after": bool(offer_after.get("listingDescription")),
  "next_step": "read_visual_result_and_archive_improved_baseline_v1"
}

Path(r"storage\exports\live_improvement_update_v1_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("LIVE_IMPROVEMENT_UPDATE_V1_FINAL_AUDIT")
print("status =", out["status"])
print("decision =", out["decision"])
print("inventory_put_status =", out["inventory_put_status"])
print("inventory_read_status =", out["inventory_read_status"])
print("offer_put_status =", out["offer_put_status"])
print("offer_read_status =", out["offer_read_status"])
print("inventory_title_after =", out["inventory_title_after"])
print("inventory_image_count_after =", out["inventory_image_count_after"])
print("offer_price_after =", out["offer_price_after"])
print("offer_has_description_after =", out["offer_has_description_after"])
print("next_step =", out["next_step"])
