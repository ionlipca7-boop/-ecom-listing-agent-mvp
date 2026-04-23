import json
import requests
from pathlib import Path

def read_text(p):
    return Path(p).read_text(encoding="utf-8").strip()

def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

base = Path(".")
token = read_text(base / "storage" / "secrets" / "ebay_access_token.txt")
offer_id = "153365657011"
sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
eps = load_json(base / "storage" / "exports" / "eps_upload_queue_v1_result.json")

image_urls = ["https://i.ebayimg.com/images/g/7MsAAeSw7kpp4-UD/s-l1600.webp"]
for r in eps.get("eps_successes", []):
    if r.get("eps_url"):
        image_urls.append(r["eps_url"])

url = "https://api.ebay.com/sell/inventory/v1/offer/" + offer_id
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE",
    "Accept": "application/json"
}

r1 = requests.get(url, headers=headers, timeout=60)
offer = r1.json() if r1.ok else {}

payload = offer.copy()
payload["imageUrls"] = image_urls
payload["sku"] = sku

r2 = requests.put(url, headers=headers, json=payload, timeout=60)
r3 = requests.get(url, headers=headers, timeout=60)
offer2 = r3.json() if r3.ok else {}

images_after = offer2.get("imageUrls", [])

out = {
  "status": "OK" if r2.status_code in [200,204] else "FAILED",
  "decision": "offer_revise_after_multi_image_inventory_update_v1_executed",
  "put_status": r2.status_code,
  "read_status": r3.status_code,
  "images_sent": len(image_urls),
  "live_image_count": len(images_after),
  "next_step": "DONE_LISTING_FULLY_READY_V1" if len(images_after)==9 else "inspect_offer_image_failure_v1"
}

Path(r"storage\exports\offer_revise_after_multi_image_inventory_update_v1_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("OFFER_REVISE_AFTER_MULTI_IMAGE_INVENTORY_UPDATE_V1_FINAL_AUDIT")
print("status =", out["status"])
print("put_status =", out["put_status"])
print("read_status =", out["read_status"])
print("images_sent =", out["images_sent"])
print("live_image_count =", out["live_image_count"])
print("next_step =", out["next_step"])
