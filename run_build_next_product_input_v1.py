import json
from pathlib import Path

EXPORTS_DIR = Path("storage") / "exports"
OUTPUT_FILE = EXPORTS_DIR / "next_product_input_v1.json"

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "sku": "ECOM-NEXT-SKU-001",
        "title": "USB-C Ladekabel 2m 60W Schnellladen",
        "description": "USB-C Kabel 2m fuer Schnellladen und Datentransfer.",
        "image_url": "REPLACE_IMAGE_URL",
        "price_value": "5.49",
        "currency": "EUR",
        "quantity": 10,
        "categoryId": "44932",
        "merchantLocationKey": "ECOM_DE_LOC_1",
        "marketplaceId": "EBAY_DE",
        "format": "FIXED_PRICE",
        "listingDuration": "GTC",
        "brand": "Markenlos",
        "mpn": "Nicht zutreffend",
        "produktart": "USB-Kabel",
        "herstellernummer": "Nicht zutreffend"
    }
    OUTPUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("BUILD_NEXT_PRODUCT_INPUT_V1_DONE")
    print("output_file =", OUTPUT_FILE)

if __name__ == "__main__":
    main()
