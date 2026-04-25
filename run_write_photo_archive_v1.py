import json
from pathlib import Path
p = Path(r"storage\memory\archive\photo_source_archive_v1.json")
data = {
  "status": "OK",
  "decision": "photo_source_archived",
  "sku": "USBCOTGAdapterUSB3TypCaufUSBAq10p399",
  "item_id": "318166440509",
  "offer_id": "153365657011",
  "image_count": 9,
  "source_type": "remote_image_manifest",
  "rule": "photo_source_data_is_project_memory_truth_for_this_listing",
  "next_step": "build_safe_full_offer_payload_v1"
}
p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("WRITE_OK")
