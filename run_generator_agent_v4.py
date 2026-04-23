import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
def generate_titles(product):
    name = product.get("name", "")
    power = product.get("power", "")
    length = product.get("length", "")
    t1 = f"USB-C Ladekabel {length} {power} Schnellladen Datenkabel"
    t2 = f"{power} USB-C Kabel {length} Super Fast Charging Datenkabel"
    t3 = f"USB-C Kabel {length} {power} fur iPhone Samsung Xiaomi Schnellladekabel"
    return [t1[:80], t2[:80], t3[:80]]
def generate_price(product):
    base = product.get("base_price", 5.0)
    return round(base * 1.5, 2)
def generate_description(product):
    return (
        f"Hochwertiges USB-C Ladekabel mit {product.get('power')} Leistung. "
        f"Ideal fur schnelles Laden und sichere Datenubertragung im Alltag und auf Reisen." 
    )
def generate_html(product):
    return (
        f"<h2>USB-C Ladekabel</h2>" 
        f"<p><b>Schnellladen & zuverlassige Qualitat</b></p>" 
        f"<ul>" 
        f"<li>Leistung: {product.get('power')}</li>" 
        f"<li>Lange: {product.get('length')}</li>" 
        f"<li>Schnelle Datenubertragung</li>" 
        f"</ul>" 
        f"<p><b>? Hohe Qualitat<br>? Schneller Versand<br>? Top Preis-Leistung</b></p>" 
        f"<p>Weitere Produkte finden Sie in unserem Shop (bald mit direkten Links).</p>" 
    )
def detect_category(product):
    return "Kabel & Adapter"
def generate_image_plan():
    return ["Hero", "Use Case", "Benefits", "Specs", "Trust", "Close-up"]
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
    out_file = EXPORTS_DIR / "generator_output_v4.json"
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("GENERATOR_AGENT_V4_OK")
    print("output_file =", out_file)
if __name__ == "__main__":
    main()
