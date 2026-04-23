import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_v1.json"
REGISTRY_FILE = BASE_DIR / "storage" / "registry" / "products_registry_v1.json"
LIVE_AUDIT_FILE = BASE_DIR / "storage" / "exports" / "publish_existing_offer_repair_v3.json"

IMAGE_URLS = [
    "https://ae01.alicdn.com/kf/S42fabc33d69c4f5592466804c540a072T.jpg",
    "https://ae01.alicdn.com/kf/Sc68f16cdbb0e48ca9f68da607d90f55fO.jpg",
    "https://ae01.alicdn.com/kf/Sceae79ed63dc4d5aab039de4a52879c8r.jpg",
    "https://ae01.alicdn.com/kf/S8893d5727a1446bb860b97548ede5410X.jpg",
    "https://ae01.alicdn.com/kf/S4f8750a0169946e0b4fc1a0f1b23089aB.jpg",
    "https://ae01.alicdn.com/kf/S3a9306f37bbf44d28dcc5d7b5aaa5c7bl.jpg",
    "https://ae01.alicdn.com/kf/Sadcd253f429a49b8a3460fe75febf721R.jpg",
    "https://ae01.alicdn.com/kf/Se63d8168e9664e28b5c0878026e2445an.jpg",
    "https://ae01.alicdn.com/kf/S21d6d1cf19c341c7928d286cd6a6e8957.jpg"
]

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def unique_append_dict(items, new_item, keys):
    for item in items:
        if all(item.get(k) == new_item.get(k) for k in keys):
            item.update(new_item)
            return items
    items.append(new_item)
    return items

def main():
    memory = read_json(MEMORY_FILE)
    live = read_json(LIVE_AUDIT_FILE)
    registry = read_json(REGISTRY_FILE) if REGISTRY_FILE.exists() else {"products": []}
    memory["updated_at_utc"] = datetime.now(UTC).isoformat()
    memory["decision"] = "project_memory_updated_after_second_live"
    live_listings = memory.get("live_listings", [])
    live_entry = {
        "product_key": live.get("product_key"),
        "sku": live.get("sku"),
        "offerId": live.get("offerId"),
        "listingId": live.get("listingId"),
        "pipeline_status": "LIVE_OK",
        "listing_state": "LIVE",
        "image_count": live.get("image_count")
    }
    memory["live_listings"] = unique_append_dict(live_listings, live_entry, ["product_key"])
    resolved = memory.get("resolved_errors", [])
    resolved = unique_append_dict(resolved, {"error": "Das Artikelmerkmal Marke fehlt", "cause": "required item specific Marke missing at publish", "solution": "add aspects Marke with fallback value No-Name before publish", "tags": ["publish", "marke", "aspects", "required-field"]}, ["error"])
    resolved = unique_append_dict(resolved, {"error": "Fugen Sie mindestens 1 Foto hinzu", "cause": "imageUrls missing at publish", "solution": "add one or more valid imageUrls before publish", "tags": ["publish", "photo", "imageUrls", "required-field"]}, ["error"])
    memory["resolved_errors"] = resolved
    media_sources = memory.get("media_sources", [])
    media_entry = {"product_key": "adapter_001", "source_type": "image_urls", "image_count": len(IMAGE_URLS), "image_urls": IMAGE_URLS, "updated_at_utc": datetime.now(UTC).isoformat()}
    memory["media_sources"] = unique_append_dict(media_sources, media_entry, ["product_key", "source_type"])
    best = memory.get("best_working_paths", [])
    best = [x for x in best if x != "publish existing offer after adding Marke and imageUrls"]
    best.append("publish existing offer after adding Marke and imageUrls")
    memory["best_working_paths"] = best
    memory["registry_snapshot"] = registry
    memory["next_target"] = {"product_key": None, "input_file": None, "goal": "choose next product"}
    MEMORY_FILE.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")
    print("MEMORY_UPDATE_AFTER_LIVE_OK")
    print("decision =", memory["decision"])
    print("live_listings_count =", len(memory.get("live_listings", [])))
    print("resolved_errors_count =", len(memory.get("resolved_errors", [])))
    print("media_sources_count =", len(memory.get("media_sources", [])))

if __name__ == "__main__":
    main()
