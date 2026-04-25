import json
from pathlib import Path

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return json.loads(path.read_text(encoding="utf-8-sig"))

archive_path = Path(r"storage\memory\archive\photo_source_archive_v2.json")
source_path = Path(r"storage\exports\safe_full_offer_payload_v1.json")
out_path = Path(r"storage\exports\safe_full_offer_payload_v2.json")

archive = load_json(archive_path)
source = load_json(source_path)

payload = source.get("payload", {})
payload["imageUrls"] = archive.get("image_urls", [])

missing = []
try:
    price_value = payload["pricingSummary"]["price"]["value"]
except Exception:
    price_value = None
if price_value in [None, ""]: missing.append("price")
if not payload.get("listingPolicies"): missing.append("listingPolicies")
if not payload.get("merchantLocationKey"): missing.append("merchantLocationKey")
if not payload.get("listingDescription"): missing.append("listingDescription")
if payload.get("availableQuantity") in [None, ""]: missing.append("availableQuantity")
if not payload.get("imageUrls"): missing.append("imageUrls")

result = {
  "status": "OK",
  "decision": "safe_full_offer_payload_v2_built",
  "sku": archive["sku"],
  "item_id": archive["item_id"],
  "offer_id": archive["offer_id"],
  "critical_fields_present": {
    "price": "price" not in missing,
    "listingPolicies": "listingPolicies" not in missing,
    "merchantLocationKey": "merchantLocationKey" not in missing,
    "listingDescription": "listingDescription" not in missing,
    "availableQuantity": "availableQuantity" not in missing,
    "imageUrls": "imageUrls" not in missing
  },
  "missing_fields": missing,
  "payload": payload,
  "rule": "no_partial_offer_updates_use_full_payload",
  "next_step": "build_real_full_offer_revise_v1"
}

out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("SAFE_FULL_OFFER_PAYLOAD_V2_OK")
print("sku =", result["sku"])
print("image_urls_count =", len(payload.get("imageUrls", [])))
print("missing_fields =", ",".join(result["missing_fields"]) if result["missing_fields"] else "none")
print("next_step =", result["next_step"])
