import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
LIVE_PATH = EXPORT_DIR / "adapter_001_live_inventory_fetch_v1.json"
OUT_PATH = EXPORT_DIR / "adapter_001_live_image_guard_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    live = load_json(LIVE_PATH)
    response = live.get("response", {})
    product = response.get("product", {})
    image_urls = product.get("imageUrls", [])
    result = {
        "status": "OK",
        "product_key": "adapter_001",
        "has_live_images": has_live_images,
        "live_image_count": len(image_urls),
        "live_image_urls": image_urls,
        "decision": "merge_live_images_into_full_revise_payload" if has_live_images else "stop_and_do_not_send_placeholder_only_payload"
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("LIVE_IMAGE_GUARD_V1")
    print("status =", result["status"])
    print("product =", result["product_key"])
    print("has_live_images =", result["has_live_images"])
    print("live_image_count =", result["live_image_count"])
    print("decision =", result["decision"])

if __name__ == "__main__":
    main()
