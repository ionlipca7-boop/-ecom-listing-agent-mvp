import json
from pathlib import Path

EXPORTS_DIR = Path("storage") / "exports"
SECRETS_DIR = Path("storage") / "secrets"
INPUT_FILE = EXPORTS_DIR / "next_product_input_v1.json"
IMAGE_FILE = SECRETS_DIR / "ebay_test_image_url.txt"
OUTPUT_FILE = EXPORTS_DIR / "next_product_input_v1.json"
AUDIT_FILE = EXPORTS_DIR / "next_product_input_image_set_audit_v1.json"

def read_text(path):
    return path.read_text(encoding="utf-8-sig").strip()

def main():
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    image_url = read_text(IMAGE_FILE)
    data["image_url"] = image_url
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {
        "status": "IMAGE_URL_SET",
        "image_url": image_url,
        "target_file": str(OUTPUT_FILE)
    }
    AUDIT_FILE.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SET_NEXT_PRODUCT_IMAGE_URL_V1_DONE")
    print("image_url =", image_url)

if __name__ == "__main__":
    main()
