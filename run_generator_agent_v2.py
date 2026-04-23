import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
def generate_title(product):
    name = product.get("name", "")
    power = product.get("power", "")
    length = product.get("length", "")
    extra = product.get("extra", "")
    parts = [name, length, power, extra]
    title = " ".join([p for p in parts if p])
    return title[:80]
def generate_price(product):
    base = product.get("base_price", 5.0)
    multiplier = product.get("market_factor", 1.3)
    return round(base * multiplier, 2)
def generate_description(product):
    return (
        f"{product.get('name')} mit {product.get('power')} Leistung. "
        f"Lange: {product.get('length')}. "
        f"Ideal fur Alltag, Reisen und schnelles Laden."
    )
def generate_html(product):
    return (
        f"<h2>{product.get('name')}</h2>"
        f"<ul>" 
        f"<li>Leistung: {product.get('power')}</li>" 
        f"<li>Lange: {product.get('length')}</li>" 
        f"<li>Schnellladen unterstutzt</li>" 
        f"</ul>" 
    )
def detect_category(product):
    name = product.get("name", "").lower()
    if "kabel" in name or "usb" in name:
        return "Kabel & Adapter"
    if "lampe" in name or "licht" in name:
        return "Beleuchtung"
    if "auto" in name:
        return "Auto Zubehor"
    return "Sonstige"
def generate_image_plan():
    return ["Hero", "Use Case", "Specs", "Comparison", "Close-up"]
def main():
    product = {
        "name": "USB-C Ladekabel",
        "power": "60W",
        "length": "2m",
        "extra": "Schnellladen",
        "base_price": 4.5,
        "market_factor": 1.4
    }
    result = {
        "title": generate_title(product),
        "price": generate_price(product),
        "description": generate_description(product),
        "html": generate_html(product),
        "category": detect_category(product),
        "images": generate_image_plan()
    }
    out_file = EXPORTS_DIR / "generator_output_v2.json"
    out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("GENERATOR_AGENT_V2_OK")
    print("output_file =", out_file)
if __name__ == "__main__":
    main()
