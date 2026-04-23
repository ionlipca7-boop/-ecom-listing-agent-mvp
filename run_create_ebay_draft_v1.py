import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

INPUT_FILE = EXPORTS_DIR / "generator_output_v5.json"
OUTPUT_FILE = EXPORTS_DIR / "ebay_draft_v1.json"


def load_generator():
    return json.loads(INPUT_FILE.read_text(encoding="utf-8"))


def build_ebay_payload(data):
    return {
        "title": data["main_title"],
        "description": data["html"],
        "price": data["price"],
        "currency": "EUR",
        "quantity": 10,
        "format": "FIXED_PRICE",
        "category_hint": "Kabel & Adapter",
        "status": "DRAFT"
    }


def main():
    data = load_generator()

    payload = build_ebay_payload(data)

    OUTPUT_FILE.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("EBAY_DRAFT_V1_OK")
    print("output_file =", OUTPUT_FILE)


if __name__ == "__main__":
    main()