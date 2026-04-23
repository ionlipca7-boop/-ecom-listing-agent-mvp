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

def as_list(v):
    if v is None: return []
    if isinstance(v, list): return v
    return [v]

base = Path(".")
token = read_text(base / "storage" / "secrets" / "ebay_access_token.txt")
sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
offer_id = "153365657011"
photo_archive = load_json(base / "storage" / "memory" / "archive" / "photo_source_archive_v2.json")
safe_offer = load_json(base / "storage" / "exports" / "safe_full_offer_payload_v2.json")

h_json = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "Content-Language": "de-DE", "Accept": "application/json"}
h_auth = {"Authorization": "Bearer " + token, "Accept": "application/json"}

offer_url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
inv_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
tree_url = "https://api.ebay.com/commerce/taxonomy/v1/get_default_category_tree_id?marketplace_id=EBAY_DE"

r_offer = requests.get(offer_url, headers=h_auth, timeout=60)
offer_live = r_offer.json() if r_offer.ok else {}
category_id = str(offer_live.get("categoryId") or safe_offer.get("payload", {}).get("categoryId") or "")

r_tree = requests.get(tree_url, headers=h_auth, timeout=60)
tree_data = r_tree.json() if r_tree.ok else {}
category_tree_id = str(tree_data.get("categoryTreeId") or "0")
aspects_url = "https://api.ebay.com/commerce/taxonomy/v1/category_tree/" + category_tree_id + "/get_item_aspects_for_category?category_id=" + category_id
r_aspects = requests.get(aspects_url, headers=h_auth, timeout=60)
aspects_data = r_aspects.json() if r_aspects.ok else {}
required_aspects = []
for a in aspects_data.get("aspects", []):
    c = a.get("aspectConstraint", {})
    if c.get("aspectRequired") is True:
        required_aspects.append(a.get("localizedAspectName"))

r_inv = requests.get(inv_url, headers=h_auth, timeout=60)
inv_live = r_inv.json() if r_inv.ok else {}
product_live = inv_live.get("product", {}) if isinstance(inv_live, dict) else {}
aspects_live = product_live.get("aspects", {}) if isinstance(product_live.get("aspects", {}), dict) else {}

if "Marke" in required_aspects and not aspects_live.get("Marke"):
    aspects_live["Marke"] = ["Markenlos"]
if "Herstellernummer" in required_aspects and not aspects_live.get("Herstellernummer"):
    aspects_live["Herstellernummer"] = ["Nicht zutreffend"]
if "MPN" in required_aspects and not aspects_live.get("MPN"):
    aspects_live["MPN"] = ["Nicht zutreffend"]

product_new = {}
if product_live.get("title"): product_new["title"] = product_live["title"]
if product_live.get("description"): product_new["description"] = product_live["description"]
product_new["aspects"] = aspects_live
product_new["imageUrls"] = photo_archive.get("image_urls", [])

inv_payload = {}
if inv_live.get("availability"): inv_payload["availability"] = inv_live["availability"]
if inv_live.get("condition"): inv_payload["condition"] = inv_live["condition"]
if inv_live.get("packageWeightAndSize"): inv_payload["packageWeightAndSize"] = inv_live["packageWeightAndSize"]
inv_payload["product"] = product_new

r_inv_put = requests.put(inv_url, headers=h_json, json=inv_payload, timeout=60)
inv_put_json = None
try:
    inv_put_json = r_inv_put.json()
except Exception:
    pass

offer_payload = safe_offer["payload"]
offer_payload["pricingSummary"]["price"]["value"] = "4.01"
r_offer_put = None
offer_put_json = None
if r_inv_put.status_code in [200, 204]:
    r_offer_put = requests.put(offer_url, headers=h_json, json=offer_payload, timeout=60)
    try:
        offer_put_json = r_offer_put.json()
    except Exception:
        pass

out = {
  "status": "OK" if (r_inv_put.status_code in [200,204] and r_offer_put is not None and r_offer_put.status_code in [200,204]) else "PARTIAL_OR_FAILED",
  "decision": "official_rules_full_revise_v1_executed",
  "sku": sku,
  "offer_id": offer_id,
  "category_id": category_id,
  "category_tree_id": category_tree_id,
  "required_aspects": required_aspects,
  "inventory_read_status": r_inv.status_code,
  "inventory_update_status": r_inv_put.status_code,
  "offer_update_status": (r_offer_put.status_code if r_offer_put is not None else None),
  "images_sent": len(product_new.get("imageUrls", [])),
  "price_sent": "4.01",
  "inventory_error_text": r_inv_put.text[:2000],
  "inventory_error_json": inv_put_json,
  "offer_error_text": (r_offer_put.text[:2000] if r_offer_put is not None else ""),
  "offer_error_json": offer_put_json,
  "next_step": "read_live_offer_after_official_rules_update_v1" if (r_inv_put.status_code in [200,204] and r_offer_put is not None and r_offer_put.status_code in [200,204]) else "inspect_exact_remaining_required_fields_v1"
}
Path(r"storage\exports\official_rules_full_revise_v1_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("OFFICIAL_RULES_FULL_REVISE_V1_FINAL_AUDIT")
print("status =", out["status"])
print("decision =", out["decision"])
print("category_id =", out["category_id"])
print("required_aspects =", ",".join(out["required_aspects"]) if out["required_aspects"] else "none")
print("inventory_read_status =", out["inventory_read_status"])
print("inventory_update_status =", out["inventory_update_status"])
print("offer_update_status =", out["offer_update_status"])
print("images_sent =", out["images_sent"])
print("price_sent =", out["price_sent"])
print("next_step =", out["next_step"])
