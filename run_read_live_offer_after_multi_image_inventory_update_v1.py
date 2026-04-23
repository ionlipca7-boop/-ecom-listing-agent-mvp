import json
import requests
from pathlib import Path

def read_text(p):
    return Path(p).read_text(encoding="utf-8").strip()

base = Path(".")
token = read_text(base / "storage" / "secrets" / "ebay_access_token.txt")
offer_id = "153365657011"

url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
headers = {
    "Authorization": "Bearer " + token,
    "Content-Language": "de-DE",
    "Accept": "application/json"
}

r = requests.get(url, headers=headers, timeout=60)
data = r.json() if r.ok else {}

price = None
try:
    price = data["pricingSummary"]["price"]["value"]
except Exception:
    pass

images = data.get("imageUrls", [])

out = {
  "status": "OK" if r.status_code == 200 else "FAILED",
  "decision": "read_live_offer_after_multi_image_inventory_update_v1_executed",
  "offer_id": offer_id,
  "http_status": r.status_code,
  "live_price": price,
  "image_count": len(images),
  "has_listingPolicies": bool(data.get("listingPolicies")),
  "has_location": bool(data.get("merchantLocationKey")),
  "has_description": bool(data.get("listingDescription")),
  "next_step": "done_listing_working_baseline_v1" if len(images) == 9 else "offer_revise_after_multi_image_inventory_update_v1"
}

Path(r"storage\exports\read_live_offer_after_multi_image_inventory_update_v1_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("READ_LIVE_OFFER_AFTER_MULTI_IMAGE_INVENTORY_UPDATE_V1_FINAL_AUDIT")
print("status =", out["status"])
print("decision =", out["decision"])
print("http_status =", out["http_status"])
print("live_price =", out["live_price"])
print("image_count =", out["image_count"])
print("has_listingPolicies =", out["has_listingPolicies"])
print("has_location =", out["has_location"])
print("has_description =", out["has_description"])
print("next_step =", out["next_step"])
