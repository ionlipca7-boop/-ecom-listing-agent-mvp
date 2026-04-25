import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
def generate_titles(product):
    name = product.get("name", "")
    power = product.get("power", "")
    length = product.get("length", "")
    t1 = f"{name} {length} {power} Schnellladen"
    t2 = f"{power} {name} {length} - Fast Charging Kabel"
    t3 = f"{name} {length} {power} fur iPhone Samsung Xiaomi"
    return [t1[:80], t2[:80], t3[:80]]
def generate_price(product):
    base = product.get("base_price", 5.0)
    return round(base * 1.4, 2)
def generate_description(product):
    return (
        f"Hochwertiges {product.get('name')} mit {product.get('power')} Leistung. "
        f"Perfekt fur schnelles Laden und zuverlassige Nutzung im Alltag." 
    )
def generate_html(product):
    return (
        f"<h2>{product.get('name')}</h2>" 
        f"<p><b>Schnelles Laden & hohe Qualitat</b></p>" 
        f"<ul>" 
        f"<li>Leistung: {product.get('power')}</li>" 
        f"<li>Lange: {product.get('length')}</li>" 
        f"<li>Kompatibel mit vielen Geraten</li>" 
        f"</ul>" 
        f"<p>Weitere Produkte finden Sie in unserem Shop.</p>" 
    )
def detect_category(product):
    name = product.get("name", "").lower()
    if "kabel" in name: return "Kabel & Adapter"
    return "Sonstige"
def generate_image_plan():
    return ["Hero", "Use Case", "Benefits", "Specs", "Close-up"]
def main():
    product = {
        "name": "USB-C Ladekabel",
        "power": "60W",
        "length": "2m",
        "base_price": 4.5
    }
    titles = generate_titles(product)
    result = {
        "titles": titles,
        "main_title": titles[0],
        "price": generate_price(product),
        "description": generate_description(product),
        "html": generate_html(product),
        "category": detect_category(product),
        "images": generate_image_plan()
    }
    out_file = EXPORTS_DIR / "generator_output_v3.json"
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("GENERATOR_AGENT_V3_OK")
    print("output_file =", out_file)
if __name__ == "__main__":
    main()
