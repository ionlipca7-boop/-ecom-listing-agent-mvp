import json
from pathlib import Path

EXECUTION_FILE = Path("upload_execution_v3.json")
OUTPUT_FILE = Path("ebay_api_payload_v1.json")


def main():
    if not EXECUTION_FILE.exists():
        print("ERROR: execution file not found")
        return

    with open(EXECUTION_FILE, "r", encoding="utf-8") as f:
        execution = json.load(f)

    if execution.get("execution_status") != "READY_FOR_REAL_API":
        print("BLOCKED: NOT READY FOR API")
        return

    # --- MOCK PAYLOAD ---
    payload = {
        "title": "USB-C Ladekabel 2m 60W Schnellladen",
        "description": "USB-C Kabel | 60W | 2m | Schnellladen",
        "price": 5.5,
        "category": "Kabel & Adapter",
        "condition": "New",
        "format": "FixedPrice"
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("EBAY API PREPARE:")
    print("payload ready")
    print(f"file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()