import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SNAPSHOT_PATH = BASE_DIR / "storage" / "exports" / "adapter_001_live_inventory_item_v1.json"
def main():
    data = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    product = data.get("product", {})
    image_urls = product.get("imageUrls", [])
    print("ADAPTER_001_LIVE_IMAGES_AUDIT")
    print("sku =", data.get("sku"))
    print("product_keys =", list(product.keys()))
    print("image_urls_count =", len(image_urls))
    print("image_urls =", json.dumps(image_urls, ensure_ascii=False))
if __name__ == "__main__":
    main()
