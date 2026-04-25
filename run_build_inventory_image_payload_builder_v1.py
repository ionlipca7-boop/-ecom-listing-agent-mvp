import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "photo_set_builder_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "inventory_image_payload_builder_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    baseline_set = source.get("baseline_set", [])

    image_urls = []
    for item in baseline_set:
        slot = item.get("slot")
        image_urls.append("EPS_IMAGE_SLOT_" + str(slot))

    result = {
        "status": "OK",
        "decision": "inventory_image_payload_builder_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "inventory_image_payload_builder_version": "v1",
        "sku": source.get("sku"),
        "offer_id": source.get("offer_id"),
        "image_count": len(image_urls),
        "imageUrls": image_urls,
        "payload_contract": {
            "inventory_full_payload_required": True,
            "images_included": True,
            "preserve_existing_images": True,
            "live_write_now": False
        },
        "next_step": "build_post_inventory_read_verification_v1"
    }

    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("INVENTORY_IMAGE_PAYLOAD_BUILDER_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = inventory_image_payload_builder_v1_built")
    print("sku =", result["sku"])
    print("image_count =", result["image_count"])
    print("images_included =", result["payload_contract"]["images_included"])
    print("live_write_now =", result["payload_contract"]["live_write_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
