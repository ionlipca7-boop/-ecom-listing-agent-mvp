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
src = load_json(base / "storage" / "exports" / "safe_full_offer_payload_v2.json")
offer_id = src["offer_id"]
payload = src["payload"]
payload["pricingSummary"]["price"]["value"] = "4.01"

url = "https://api.ebay.com/sell/inventory/v1/offer/" + str(offer_id)
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE",
    "Accept": "application/json"
}

r_put = requests.put(url, headers=headers, json=payload, timeout=60)
r_get = requests.get(url, headers={"Authorization": "Bearer " + token, "Content-Language": "de-DE", "Accept": "application/json"}, timeout=60)
live = r_get.json() if r_get.ok else {}

price = None
try:
    price = live["pricingSummary"]["price"]["value"]
except Exception:
    pass

out = {
    "status": "OK" if (r_put.status_code in [200,204] and r_get.status_code == 200) else "FAILED",
    "decision": "offer_revise_after_inventory_fix_v1_executed",
    "sku": src["sku"],
    "offer_id": offer_id,
    "put_status": r_put.status_code,
    "read_status": r_get.status_code,
    "live_price": price,
    "has_listingPolicies": bool(live.get("listingPolicies")),
    "has_location": bool(live.get("merchantLocationKey")),
    "has_description": bool(live.get("listingDescription")),
    "next_step": "build_hosted_multi_image_source_v1" if (r_put.status_code in [200,204] and r_get.status_code == 200) else "inspect_offer_revise_error_v1"
}
Path(r"storage\exports\offer_revise_after_inventory_fix_v1_result.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("OFFER_REVISE_AFTER_INVENTORY_FIX_V1_FINAL_AUDIT")
print("status =", out["status"])
print("decision =", out["decision"])
print("put_status =", out["put_status"])
print("read_status =", out["read_status"])
print("live_price =", out["live_price"])
print("has_listingPolicies =", out["has_listingPolicies"])
print("has_location =", out["has_location"])
print("has_description =", out["has_description"])
print("next_step =", out["next_step"])
