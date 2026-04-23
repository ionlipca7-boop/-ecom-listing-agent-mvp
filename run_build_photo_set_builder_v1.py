import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "photo_source_registry_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "photo_set_builder_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    slots = source.get("photo_slots", [])
    baseline_set = []
    variant_ready_set = []
    for item in slots:
        slot_no = item.get("slot")
        baseline_set.append({
            "slot": slot_no,
            "role": "baseline_eps",
            "status": "active",
            "reuse_allowed": True
        })
        variant_ready_set.append({
            "slot": slot_no,
            "role": "variant_reuse_candidate",
            "status": "ready",
            "replace_only_if_better": True
        })
    result = {
        "status": "OK",
        "decision": "photo_set_builder_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "photo_set_builder_version": "v1",
        "sku": source.get("sku"),
        "offer_id": source.get("offer_id"),
        "baseline_image_count": source.get("baseline_image_count", 0),
        "baseline_set": baseline_set,
        "variant_ready_set": variant_ready_set,
        "builder_contract": {
            "preserve_baseline_order": True,
            "allow_multi_listing_reuse": True,
            "require_inventory_read_before_live_apply": True,
            "live_write_now": False
        },
        "next_step": "build_inventory_image_payload_builder_v1"
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PHOTO_SET_BUILDER_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = photo_set_builder_v1_built")
    print("sku =", result["sku"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("baseline_set_count =", len(result["baseline_set"]))
    print("variant_ready_count =", len(result["variant_ready_set"]))
    print("live_write_now =", result["builder_contract"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
