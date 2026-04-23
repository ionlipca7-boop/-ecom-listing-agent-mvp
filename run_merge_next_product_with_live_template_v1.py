import json
from copy import deepcopy
from pathlib import Path

EXPORTS_DIR = Path("storage") / "exports"
TEMPLATE_FILE = EXPORTS_DIR / "ebay_live_template_v1.json"
INPUT_FILE = EXPORTS_DIR / "next_product_input_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "ebay_next_merged_payload_v1.json"

def main():
    template = json.loads(TEMPLATE_FILE.read_text(encoding="utf-8"))
    product_input = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    merged = deepcopy(template)

    merged["inventory_item"]["sku"] = product_input["sku"]
    merged["inventory_item"]["availability"]["shipToLocationAvailability"]["quantity"] = product_input["quantity"]
    merged["inventory_item"]["product"]["title"] = product_input["title"]
    merged["inventory_item"]["product"]["description"] = product_input["description"]
    merged["inventory_item"]["product"]["imageUrls"] = [product_input["image_url"]]
    merged["inventory_item"]["product"]["brand"] = product_input["brand"]
    merged["inventory_item"]["product"]["mpn"] = product_input["mpn"]
    merged["inventory_item"]["product"]["aspects"]["Produktart"] = [product_input["produktart"]]
    merged["inventory_item"]["product"]["aspects"]["Marke"] = [product_input["brand"]]
    merged["inventory_item"]["product"]["aspects"]["Herstellernummer"] = [product_input["herstellernummer"]]

    merged["offer"]["sku"] = product_input["sku"]
    merged["offer"]["marketplaceId"] = product_input["marketplaceId"]
    merged["offer"]["format"] = product_input["format"]
    merged["offer"]["availableQuantity"] = product_input["quantity"]
    merged["offer"]["categoryId"] = product_input["categoryId"]
    merged["offer"]["merchantLocationKey"] = product_input["merchantLocationKey"]
    merged["offer"]["listingDuration"] = product_input["listingDuration"]
    merged["offer"]["pricingSummary"]["price"]["value"] = product_input["price_value"]
    merged["offer"]["pricingSummary"]["price"]["currency"] = product_input["currency"]

    merged["merge_meta"] = {
        "status": "MERGED_READY",
        "source_template": str(TEMPLATE_FILE),
        "source_input": str(INPUT_FILE)
    }

    OUTPUT_FILE.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print("MERGE_NEXT_PRODUCT_WITH_TEMPLATE_V1_DONE")
    print("output_file =", OUTPUT_FILE)
    print("sku =", merged["inventory_item"]["sku"])

if __name__ == "__main__":
    main()
