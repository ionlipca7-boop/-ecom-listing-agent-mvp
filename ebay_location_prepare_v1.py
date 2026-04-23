import json
from pathlib import Path

OUTPUT_FILE = Path("ebay_location_payload_v1.json")


def main():
    payload = {
        "name": "Main Warehouse Germany",
        "location": {
            "address": {
                "addressLine1": "Sample Street 1",
                "city": "Berlin",
                "postalCode": "10115",
                "country": "DE"
            }
        },
        "locationTypes": [
            "WAREHOUSE"
        ]
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("LOCATION PAYLOAD CREATED:")
    print(f"file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()