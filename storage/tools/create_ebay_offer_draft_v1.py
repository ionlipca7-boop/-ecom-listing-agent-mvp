import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/"storage/state_control/create_new_listing_payload_v1.json"
OUT=ROOT/"storage/state_control/create_ebay_offer_draft_v1.json"
data=json.loads(SRC.read_text(encoding="utf-8-sig"))
b=data["listing_result"]["final_listing_bundle"]
r={"status":"READY_DRAFT_ONLY","publish_called":False,"offer_draft":{"title":b["title"],"category":b["category"],"price":b["price"],"description":b["description"],"item_specifics":b["item_specifics"],"images":b["images"],"approval_status":"PENDING_APPROVAL"}}
OUT.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
print("OK")