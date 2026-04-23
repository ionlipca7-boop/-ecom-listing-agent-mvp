import json
from pathlib import Path

AUDIT_PATH = Path("storage/exports/control_action_get_live_status_audit_v2.json")

def main():
    data = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    snap = data.get("inventory_snapshot", {})
    product = snap.get("product", {}) if isinstance(snap, dict) else {}
    raw_images = product.get("imageUrls") if isinstance(product, dict) else []
    if isinstance(raw_images, list):
        image_count = len([x for x in raw_images if isinstance(x, str) and x.strip()])
    if isinstance(raw_images, str):
        if raw_images.strip():
            image_count = 
    print("DEBUG_IMAGE_COUNT_FROM_SNAPSHOT")
    print("raw_images_type =", type(raw_images).__name__)
    print("raw_images_value =", raw_images)
    print("image_count =", image_count)

if __name__ == "__main__":
    main()
