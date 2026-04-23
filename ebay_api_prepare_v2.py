import json
from pathlib import Path

EXECUTION_FILE = Path("upload_execution_v3.json")
OUTPUT_FILE = Path("ebay_api_payload_v2.json")


def main():
    if not EXECUTION_FILE.exists():
        print("ERROR: execution file not found")
        return

    with open(EXECUTION_FILE, "r", encoding="utf-8") as f:
        execution = json.load(f)

    if execution.get("execution_status") != "READY_FOR_REAL_API":
        print("BLOCKED: NOT READY FOR API")
        return

    # --- REALISTIC EBAY STRUCTURE ---
    payload = {
        "title": "USB-C Ladekabel 2m 60W Schnellladen",
        "description": "USB-C Kabel | 60W | 2m | Schnellladen",
        "price": {
            "value": "5.50",
            "currency": "EUR"
        },
        "quantity": 10,
        "categoryId": "58058",  # пример: Kabel & Adapter
        "condition": "NEW",
        "listingFormat": "FIXED_PRICE",
        "country": "DE",
        "shippingOptions": [
            {
                "service": "DHL",
                "cost": "0.00"
            }
        ],
        "itemSpecifics": {
            "Marke": "Markenlos",
            "Kabellänge": "2m",
            "Leistung": "60W",
            "Anschluss": "USB-C"
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("EBAY API PREPARE V2:")
    print("payload ready (real structure)")
    print(f"file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()