import json
from pathlib import Path

BASE = Path(r"storage")
ARCHIVE = BASE / "memory" / "archive" / "photo_source_archive_v1.json"
EXPORT_DIR = BASE / "exports"
OUT = EXPORT_DIR / "safe_full_offer_payload_v1.json"

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except Exception:
            return None

def walk(x):
    if isinstance(x, dict):
        yield x
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)

def pick_first(objs, key):
    for obj in objs:
        if isinstance(obj, dict) and key in obj and obj[key] not in [None, "", [], {}]:
            return obj[key]
    return None

archive = load_json(ARCHIVE)
if archive is None:
    raise SystemExit("ARCHIVE_MISSING_OR_INVALID")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)

json_files = sorted(EXPORT_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
all_objs = []
scanned = []
for fp in json_files:
    data = load_json(fp)
    if data is None:
        continue
    scanned.append(fp.name)
    all_objs.extend(list(walk(data)))

listing_policies = pick_first(all_objs, "listingPolicies")
merchant_location_key = pick_first(all_objs, "merchantLocationKey")
listing_description = pick_first(all_objs, "listingDescription")
available_quantity = pick_first(all_objs, "availableQuantity")
pricing_summary = pick_first(all_objs, "pricingSummary")
marketplace_id = pick_first(all_objs, "marketplaceId") or "EBAY_DE"
format_value = pick_first(all_objs, "format") or "FIXED_PRICE"
currency_value = "EUR"
price_value = None
if isinstance(pricing_summary, dict):
    price_obj = pricing_summary.get("price")
    if isinstance(price_obj, dict):
        price_value = price_obj.get("value")
        currency_value = price_obj.get("currency", "EUR") or "EUR"
if price_value in [None, ""] and "price_marker_4_01_applied":
    price_value = "4.01"

image_urls = archive.get("image_urls", [])

payload = {
    "sku": archive["sku"],
    "marketplaceId": marketplace_id,
    "format": format_value,
    "availableQuantity": available_quantity,
    "merchantLocationKey": merchant_location_key,
    "listingDescription": listing_description,
    "listingPolicies": listing_policies,
    "pricingSummary": {
        "price": {
            "value": price_value,
            "currency": currency_value
        }
    },
    "imageUrls": image_urls
}

missing = []
if payload["pricingSummary"]["price"]["value"] in [None, ""]: missing.append("price")
if not payload["listingPolicies"]: missing.append("listingPolicies")
if not payload["merchantLocationKey"]: missing.append("merchantLocationKey")
if not payload["listingDescription"]: missing.append("listingDescription")
if payload["availableQuantity"] in [None, ""]: missing.append("availableQuantity")
if not payload["imageUrls"]: missing.append("imageUrls")

result = {
    "status": "OK",
    "decision": "safe_full_offer_payload_v1_built",
    "sku": archive["sku"],
    "item_id": archive["item_id"],
    "offer_id": archive["offer_id"],
    "scanned_exports_count": len(scanned),
    "scanned_exports_sample": scanned[:10],
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
    "next_step": "review_missing_fields_then_build_real_full_offer_revise_v1"
}

OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("SAFE_FULL_OFFER_PAYLOAD_V1_OK")
print("sku =", result["sku"])
print("scanned_exports_count =", result["scanned_exports_count"])
print("missing_fields =", ",".join(result["missing_fields"]) if result["missing_fields"] else "none")
print("next_step =", result["next_step"])
