import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "storage" / "memory" / "project_memory_v1.json"
ACTIVE_FILE = BASE_DIR / "storage" / "memory" / "project_memory_active_v1.json"
REVIEW_FILE = BASE_DIR / "storage" / "exports" / "adapter_001_listing_review_v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def upsert_review(items, new_item):
    for item in items:
        if item.get("product_key") == new_item.get("product_key"):
            item.update(new_item)
            return items
    items.append(new_item)
    return items

def main():
    memory = read_json(MEMORY_FILE)
    active = read_json(ACTIVE_FILE)
    review = {
        "status": "OK",
        "decision": "listing_review_saved",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "product_key": "adapter_001",
        "listing_id": "318166440509",
        "review_findings": {
            "photos_need_optimization": True,
            "photos_current_state": "supplier_urls_used_without_sales_optimization",
            "title_keep_for_now": True,
            "specifics_need_expansion": True,
            "color_current_issue": "single_color_set_but_photos_show_multiple_colors",
            "description_need_html": True,
            "description_current_issue": "plain_short_text_without_sales_structure",
            "payment_policy_check_needed": True,
            "shipping_policy_check_needed": True,
            "ad_rate_target_percent": 7,
            "ad_rule_after_7_days_no_movement": "increase_by_1_percent",
            "offer_discount_min_percent": 5,
            "manual_ui_review_source": "user_screenshots_2026_04_18"
        },
        "next_optimization_blocks": [
            "photo_system_upgrade",
            "item_specifics_upgrade",
            "html_description_upgrade",
            "ad_settings_standardization",
            "offer_settings_standardization"
        ]
    }
    reviews = memory.get("listing_reviews", [])
    memory["listing_reviews"] = upsert_review(reviews, review)
    memory["updated_at_utc"] = datetime.now(UTC).isoformat()
    memory["decision"] = "listing_review_added_to_memory"
    active_reviews = active.get("listing_reviews", [])
    active["listing_reviews"] = upsert_review(active_reviews, review)
    active["updated_at_utc"] = datetime.now(UTC).isoformat()
    active["decision"] = "active_memory_updated_with_listing_review"
    write_json(MEMORY_FILE, memory)
    write_json(ACTIVE_FILE, active)
    write_json(REVIEW_FILE, review)
    print("LISTING_REVIEW_MEMORY_OK")
    print("product_key =", review["product_key"])
    print("listing_id =", review["listing_id"])
    print("ad_rate_target_percent =", review["review_findings"]["ad_rate_target_percent"])
    print("offer_discount_min_percent =", review["review_findings"]["offer_discount_min_percent"])

if __name__ == "__main__":
    main()
