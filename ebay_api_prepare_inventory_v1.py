import json
from pathlib import Path

OUTPUT_FILE = Path("ebay_inventory_payload_v1.json")


def main():
    payload = {
        "sku": "usb-c-2m-60w-001",
        "product": {
            "title": "USB-C Ladekabel 2m 60W Schnellladen",
            "description": "USB-C Kabel | 60W | 2m | Schnellladen",
            "aspects": {
                "Marke": ["Markenlos"],
                "Kabellänge": ["2m"],
                "Leistung": ["60W"],
                "Anschluss": ["USB-C"]
            }
        },
        "condition": "NEW",
        "availability": {
            "shipToLocationAvailability": {
                "quantity": 10
            }
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("INVENTORY PAYLOAD CREATED:")
    print(f"file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()