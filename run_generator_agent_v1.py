import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
def generate_title(product):
    name = product.get("name", "")
    power = product.get("power", "")
    length = product.get("length", "")
    return f"{name} {length} {power} Schnellladen USB-C Kabel".strip()
def generate_price(product):
    base = product.get("base_price", 5.0)
    return round(base * 1.2, 2)
def generate_description(product):
    return f"Produkt: {product.get('name')} | Leistung: {product.get('power')} | Lange: {product.get('length')}" 
def generate_html(product):
    return f"<h2>{product.get('name')}</h2><p>Schnellladen Kabel mit hoher Leistung.</p>"
def generate_category(product):
    return "Kabel & Adapter"
def generate_image_plan():
    return ["Hero", "Features", "Specs", "Usage", "Close-up"]
def main():
    product = {
        "name": "USB-C Ladekabel",
        "power": "60W",
        "length": "2m",
        "base_price": 4.5
    }
    result = {
        "title": generate_title(product),
        "price": generate_price(product),
        "description": generate_description(product),
        "html": generate_html(product),
        "category": generate_category(product),
        "images": generate_image_plan()
    }
    out_file = EXPORTS_DIR / "generator_output_v1.json"
    out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("GENERATOR_AGENT_V1_OK")
    print("output_file =", out_file)
if __name__ == "__main__":
    main()
