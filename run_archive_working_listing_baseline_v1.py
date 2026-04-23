import json
from pathlib import Path

def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))

base = Path(".")
src = load_json(base / "storage" / "exports" / "live_listing_snapshot_v1.json")
out_path = base / "storage" / "memory" / "archive" / "working_listing_baseline_v1.json"
out_path.parent.mkdir(parents=True, exist_ok=True)

data = {
  "date": "2026-04-18",
  "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
  "status": "OK",
  "decision": "working_listing_baseline_v1_archived",
  "sku": src["sku"],
  "offer_id": src["offer_id"],
  "item_id": src["item_id"],
  "listing_status": src.get("offer_payload", {}).get("status", ""),
  "listing_id": src.get("offer_payload", {}).get("listing", {}).get("listingId", ""),
  "price": src.get("offer_payload", {}).get("pricingSummary", {}).get("price", {}).get("value", ""),
  "currency": src.get("offer_payload", {}).get("pricingSummary", {}).get("price", {}).get("currency", ""),
  "inventory_picture_count": src.get("inventory_picture_count", 0),
  "offer_picture_count": src.get("offer_picture_count", 0),
  "inventory_image_urls": src.get("inventory_payload", {}).get("product", {}).get("imageUrls", []),
  "key_result": "live_listing_visually_confirmed_with_multiple_photos",
  "rules_confirmed": [
    "photo_path_external_to_eps_to_inventory",
    "mandatory_aspects_required_for_inventory_update",
    "offer_imageUrls_not_source_of_truth_for_this_flow",
    "inventory_plus_live_page_are_truth_for_photo_verification",
    "full_payload_preferred_over_partial_updates"
  ],
  "next_step": "improve_title_description_and_photo_order_v1"
}

out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("ARCHIVE_WORKING_LISTING_BASELINE_V1_FINAL_AUDIT")
print("status =", data["status"])
print("decision =", data["decision"])
print("sku =", data["sku"])
print("listing_status =", data["listing_status"])
print("price =", data["price"])
print("inventory_picture_count =", data["inventory_picture_count"])
print("offer_picture_count =", data["offer_picture_count"])
print("next_step =", data["next_step"])
