import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
READY_FILE = EXPORTS_DIR / "real_ebay_template_export_v1.json"
PRICE_FILE = EXPORTS_DIR / "price_optimizer_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "ai_title_optimizer_v1.json"

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
    price_data = read_json(PRICE_FILE)

    row = get_first_row(ready_data)
    optimizer_status = "WAITING"
    source_title = ""
    optimized_title = ""
    price_status = "MISSING"
    next_step = "CHECK_INPUTS_FIRST"

    if price_data:
        price_status = price_data.get("optimizer_status", "MISSING")

    if row:
        source_title = clean_text(row.get("Title"))
        product_type = clean_text(row.get("ProductType"))
        cable_length = clean_text(row.get("CableLength"))
        connectivity = clean_text(row.get("Connectivity"))
        power_part = "60W"
        if "60W" not in source_title:
            power_part = ""
        optimized_title = " ".join(part for part in (power_part, product_type, cable_length, connectivity, "Schnellladen") if part)
        optimized_title = limit_title(optimized_title, 80)
        title_length = len(optimized_title)

    if row and price_status == "READY":
        optimizer_status = "READY"
        next_step = "GENERATE_MORE_TITLE_VARIANTS_LATER"

    output = {
        "optimizer_status": optimizer_status,
        "next_step": next_step,
        "summary": {
            "price_status": price_status,
            "source_title": source_title,
            "optimized_title": optimized_title,
            "title_length": title_length,
            "max_title_length": 80
        },
        "rules": {
            "rule_1": "keep title at or below 80 chars",
            "rule_2": "prioritize power plus product type plus length",
            "rule_3": "keep high intent keyword Schnellladen"
        },
        "inputs": {
            "ready_file": str(READY_FILE),
            "price_file": str(PRICE_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("AI_TITLE_OPTIMIZER_V1:")
    print("optimizer_status:", output["optimizer_status"])
    print("source_title:", output["summary"]["source_title"])
    print("optimized_title:", output["summary"]["optimized_title"])
    print("title_length:", output["summary"]["title_length"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
