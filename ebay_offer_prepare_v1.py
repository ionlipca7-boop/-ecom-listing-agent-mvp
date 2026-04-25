import json
from pathlib import Path

OUTPUT_FILE = Path("ebay_offer_payload_v1.json")


def main():
    payload = {
        "sku": "usb-c-2m-60w-001",
        "marketplaceId": "EBAY_DE",
        "format": "FIXED_PRICE",
        "availableQuantity": 10,
        "categoryId": "58058",
        "listingDescription": "USB-C Kabel | 60W | 2m | Schnellladen",
        "pricingSummary": {
            "price": {
                "value": "5.50",
                "currency": "EUR"
            }
        },
        "listingPolicies": {
            "fulfillmentPolicyId": "YOUR_POLICY_ID",
            "paymentPolicyId": "YOUR_POLICY_ID",
            "returnPolicyId": "YOUR_POLICY_ID"
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("OFFER PAYLOAD CREATED:")
    print(f"file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()