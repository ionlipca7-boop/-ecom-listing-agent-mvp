import json
from pathlib import Path

PAYLOAD_FILE = Path("ebay_api_payload_v3.json")
OUTPUT_FILE = Path("ebay_api_mock_result_v1.json")


REQUIRED_FIELDS = [
    "title",
    "description",
    "price",
    "quantity",
    "categoryId",
    "condition",
    "listingFormat",
    "country"
]


def validate(payload):
    missing = []

    for field in REQUIRED_FIELDS:
        if field not in payload:
            missing.append(field)

    if "value" not in payload.get("price", {}):
        missing.append("price.value")

    if "currency" not in payload.get("price", {}):
        missing.append("price.currency")

    return missing


def main():
    if not PAYLOAD_FILE.exists():
        print("ERROR: payload not found")
        return

    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    missing = validate(payload)

    if missing:
        result = {
            "status": "FAILED",
            "missing_fields": missing
        }
    else:
        result = {
            "status": "SUCCESS",
            "mode": "MOCK_API",
            "message": "Payload valid. Ready for real eBay API."
        }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("EBAY API MOCK EXECUTOR:")
    print(f"status: {result['status']}")
    print(f"output_file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()