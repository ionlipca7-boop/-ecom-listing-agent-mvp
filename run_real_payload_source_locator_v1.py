import json
from pathlib import Path
ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
EXPORTS = ROOT / "storage" / "exports"

def short_keys(d):
    try:
        return list(d.keys())[:20]
    except Exception:
        return []

inventory_hits = []
offer_hits = []

for p in sorted(EXPORTS.glob("*.json")):
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue

    candidates = []
    if isinstance(data, dict):
        candidates.append(("root", data))
        for k, v in data.items():
            if isinstance(v, dict):
                candidates.append((k, v))

    for where, obj in candidates:
        keys = set(obj.keys())

        has_inventory_shape = ("availability" in keys) or ("product" in keys) or ("condition" in keys) or ("packageWeightAndSize" in keys) or ("merchantLocationKey" in keys)
        has_offer_shape = ("marketplaceId" in keys) or ("format" in keys) or ("availableQuantity" in keys) or ("listingPolicies" in keys) or ("pricingSummary" in keys)

        if has_inventory_shape:
            inventory_hits.append({"file": p.name, "where": where, "keys": short_keys(obj)})
        if has_offer_shape:
            offer_hits.append({"file": p.name, "where": where, "keys": short_keys(obj)})

print("REAL_PAYLOAD_SOURCE_LOCATOR_V1")
print("inventory_hits_count =", len(inventory_hits))
for item in inventory_hits[:20]:
    print("INVENTORY_HIT =", item)
print("offer_hits_count =", len(offer_hits))
for item in offer_hits[:20]:
    print("OFFER_HIT =", item)
print("next_step = choose_best_real_payload_source")
