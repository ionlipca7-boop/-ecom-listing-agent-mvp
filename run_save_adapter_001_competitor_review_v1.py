import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_v1.json"
ACTIVE_FILE = BASE_DIR / "storage" / "memory" / "project_memory_active_v1.json"
OUT_FILE = BASE_DIR / "storage" / "exports" / "adapter_001_competitor_review_v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def upsert(items, new_item, key_name):
    for item in items:
        if item.get(key_name) == new_item.get(key_name):
            item.update(new_item)
            return items
    items.append(new_item)
    return items

def main():
    memory = read_json(MEMORY_FILE)
    active = read_json(ACTIVE_FILE)
    review = {
        "status": "OK",
        "decision": "adapter_001_competitor_review_saved",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "product_key": "adapter_001",
        "competitor_examples": [
            {
                "source": "ebay_item_358331490487",
                "takeaways": [
                    "8 photos used",
                    "price point around 9.99 EUR",
                    "EAN fallback used",
                    "dimensions and weight shown",
                    "product type wording weaker than desired"
                ]
            },
            {
                "source": "ebay_item_236686202391",
                "takeaways": [
                    "richer specifics set",
                    "benefit-oriented fields like Besonderheiten",
                    "brand compatibility included",
                    "material and dimensions included",
                    "free shipping and free return visible"
                ]
            }
        ],
        "actionable_rules": [
            "strengthen specifics beyond minimum",
            "do not rely only on supplier photos",
            "prepare stronger HTML description",
            "keep title improvement for later test phase",
            "use competitor review as reference not copy"
        ]
    }
    reviews = memory.get("competitor_reviews", [])
    memory["competitor_reviews"] = upsert(reviews, review, "product_key")
    memory["updated_at_utc"] = datetime.now(UTC).isoformat()
    active_reviews = active.get("competitor_reviews", [])
    active["competitor_reviews"] = upsert(active_reviews, review, "product_key")
    active["updated_at_utc"] = datetime.now(UTC).isoformat()
    write_json(MEMORY_FILE, memory)
    write_json(ACTIVE_FILE, active)
    write_json(OUT_FILE, review)
    print("COMPETITOR_REVIEW_OK")
    print("product_key =", review["product_key"])
    print("competitor_examples_count =", len(review["competitor_examples"]))

if __name__ == "__main__":
    main()
