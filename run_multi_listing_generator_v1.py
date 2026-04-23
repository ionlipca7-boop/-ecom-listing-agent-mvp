import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
READY_FILE = EXPORTS_DIR / "real_ebay_template_export_v1.json"
TITLE_FILE = EXPORTS_DIR / "ai_title_optimizer_v1.json"
PRICE_FILE = EXPORTS_DIR / "price_optimizer_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "multi_listing_generator_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()

def limit_title(text, max_len):
    value = clean_text(text)
    if len(value) <= max_len:
        return value
    return value[:max_len].rstrip()

def get_first_row(data):
    if not data:
        return None
    rows = data.get("rows", [])
    if not rows:
        return None
    return rows[0]

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    ready_data = read_json(READY_FILE)
    title_data = read_json(TITLE_FILE)
    price_data = read_json(PRICE_FILE)

    row = get_first_row(ready_data)
    generator_status = "WAITING"
    next_step = "CHECK_INPUTS_FIRST"
    base_price = 0.0
    optimized_title = ""
    variants = []

    if title_data:
        optimized_title = clean_text(title_data.get("summary", {}).get("optimized_title"))

    if price_data:
        base_price = float(price_data.get("summary", {}).get("recommended_price", 0.0))

    if row:
        product_type = clean_text(row.get("ProductType"))
        cable_length = clean_text(row.get("CableLength"))
        connectivity = clean_text(row.get("Connectivity"))
        color_name = clean_text(row.get("Color"))

        variant_1_title = limit_title(optimized_title, 80)
        variant_2_title = limit_title("60W " + product_type + " " + cable_length + " Schnellladekabel", 80)
        variant_3_title = limit_title(product_type + " " + cable_length + " " + connectivity + " Kabel " + color_name, 80)

        variants.append({
            "variant_id": "VARIANT_1",
            "title": variant_1_title,
            "price": base_price,
            "angle": "baseline_ai_title"
        })

        variants.append({
            "variant_id": "VARIANT_2",
            "title": variant_2_title,
            "price": base_price,
            "angle": "schnellladen_focus"
        })

        variants.append({
            "variant_id": "VARIANT_3",
            "title": variant_3_title,
            "price": base_price,
            "angle": "compatibility_color_focus"
        })

    if row and optimized_title and base_price >= 0:
        generator_status = "READY"
        next_step = "REVIEW_VARIANTS_AND_SELECT_TEST_SET"

    output = {
        "generator_status": generator_status,
        "next_step": next_step,
        "summary": {
            "variant_count": len(variants),
            "base_price": base_price,
            "optimized_title": optimized_title
        },
        "variants": variants,
        "inputs": {
            "ready_file": str(READY_FILE),
            "title_file": str(TITLE_FILE),
            "price_file": str(PRICE_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("MULTI_LISTING_GENERATOR_V1:")
    print("generator_status:", output["generator_status"])
    print("variant_count:", output["summary"]["variant_count"])
    print("base_price:", output["summary"]["base_price"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
