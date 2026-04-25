import json
from pathlib import Path

EXPORTS_DIR = Path("storage") / "exports"
OUTPUT_FILE = EXPORTS_DIR / "ebay_live_template_v1.json"

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    template = {
        "inventory_item": {
            "sku": "REPLACE_SKU",
            "availability": {"shipToLocationAvailability": {"quantity": 10}},
            "condition": "NEW",
            "product": {
                "title": "REPLACE_TITLE",
                "description": "REPLACE_DESCRIPTION",
                "imageUrls": ["REPLACE_IMAGE_URL"],
                "brand": "Markenlos",
                "mpn": "Nicht zutreffend",
                "aspects": {
                    "Produktart": ["USB-Kabel"],
                    "Marke": ["Markenlos"],
                    "Herstellernummer": ["Nicht zutreffend"]
                }
            }
        },
        "offer": {
            "sku": "REPLACE_SKU",
            "marketplaceId": "EBAY_DE",
            "format": "FIXED_PRICE",
            "availableQuantity": 10,
            "categoryId": "44932",
            "merchantLocationKey": "ECOM_DE_LOC_1",
            "listingDuration": "GTC",
            "pricingSummary": {"price": {"value": "5.49", "currency": "EUR"}},
            "listingPolicies": {
                "fulfillmentPolicyId": "257755855024",
                "paymentPolicyId": "257755913024",
                "returnPolicyId": "257755877024"
            }
        },
        "publish_requirements_confirmed": [
            "Produktart",
            "imageUrls",
            "Marke",
            "Herstellernummer",
            "brand",
            "mpn"
        ],
        "success_reference": {
            "offerId": "152921341011",
            "listingId": "318162033369",
            "sku": "ECOM-TEST-CABLE-001"
        }
    }
    OUTPUT_FILE.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
    print("BUILD_EBAY_LIVE_TEMPLATE_V1_DONE")
    print("output_file =", OUTPUT_FILE)

if __name__ == "__main__":
    main()
