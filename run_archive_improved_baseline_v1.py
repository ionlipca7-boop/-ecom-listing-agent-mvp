import json
from pathlib import Path

def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

base = Path(".")
result = load_json(base / "storage" / "exports" / "live_improvement_update_v1_result.json")
brief = load_json(base / "storage" / "exports" / "improvement_brief_v1.json")

out = {
  "date": "2026-04-18",
  "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
  "phase": "IMPROVED_BASELINE_V1",
  "sku": result["sku"],
  "offer_id": result["offer_id"],
  "achievements": [
    "inventory_full_update_stable",
    "offer_full_update_stable",
    "image_pipeline_working_9_images",
    "title_optimized_german",
    "description_html_applied",
    "price_stable_4_01"
  ],
  "current_state": {
    "price": result["offer_price_after"],
    "image_count": result["inventory_image_count_after"],
    "title": result["inventory_title_after"]
  },
  "rules": [
    "always_use_full_payload",
    "inventory_first_then_offer",
    "never_break_working_images",
    "never_send_partial_payload",
    "eps_images_preferred"
  ],
  "next_priority": "build_photo_pipeline_and_multi_listing_system",
  "next_step": "start_new_chat_with_control_room_continuity"
}

Path(r"storage\memory\archive\improved_baseline_v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("ARCHIVE_IMPROVED_BASELINE_V1_AUDIT")
print("status = OK")
print("sku =", out["sku"])
print("price =", out["current_state"]["price"])
print("image_count =", out["current_state"]["image_count"])
print("phase =", out["phase"])
print("next_step =", out["next_step"])
