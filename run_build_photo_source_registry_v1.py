import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "photo_upgrade_pipeline_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "photo_source_registry_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    image_count = int(source.get("current_image_count", 0))
    slots = []
    for i in range(1, image_count + 1):
        slots.append({
            "slot": i,
            "source_type": "EPS",
            "status": "working_baseline",
            "reuse_allowed": True,
            "replace_only_if_better": True
        })
    result = {
        "status": "OK",
        "decision": "photo_source_registry_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "photo_source_registry_version": "v1",
        "sku": source.get("sku"),
        "offer_id": source.get("offer_id"),
        "baseline_image_count": image_count,
        "registry_mode": "safe_reuse_first",
        "source_phase": source.get("source_phase"),
        "source_rules": source.get("pipeline_rules", []),
        "photo_slots": slots,
        "multi_listing_contract": {
            "allow_reuse_across_variants": True,
            "preserve_slot_order": True,
            "require_read_before_replace": True,
            "live_write_now": False
        },
        "next_step": "build_photo_set_builder_v1"
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PHOTO_SOURCE_REGISTRY_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = photo_source_registry_v1_built")
    print("sku =", result["sku"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("registry_mode =", result["registry_mode"])
    print("live_write_now =", result["multi_listing_contract"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
