import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def fix_text(text):
    replacements = {
        "fur": "für",
        "uber": "über",
        "Lange": "Länge",
        "Qualitat": "Qualität",
        "zuverlassig": "zuverlässig"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def generate_titles(product):
    length = product.get("length", "")
    power = product.get("power", "")

    t1 = f"USB-C Ladekabel {length} {power} Schnellladen Datenkabel"
    t2 = f"{power} USB-C Kabel {length} Super Fast Charging Datenkabel"
    t3 = f"USB-C Kabel {length} {power} für iPhone Samsung Xiaomi Schnellladekabel"

    return [t1[:80], t2[:80], t3[:80]]


def generate_price(product):
    return round(product.get("base_price", 5.0) * 1.5, 2)


def generate_description(product):
    text = f"Hochwertiges USB-C Ladekabel mit {product.get('power')} Leistung. Ideal für schnelles Laden und sichere Datenübertragung im Alltag und auf Reisen."
    return fix_text(text)


def generate_html(product):
    return f"<h2>USB-C Ladekabel</h2><p><b>Schnellladen & zuverlässige Qualität</b></p><ul><li>Leistung: {product.get('power')}</li><li>Länge: {product.get('length')}</li><li>Schnelle Datenübertragung</li></ul><p><b>✔ Hohe Qualität<br>✔ Schneller Versand<br>✔ Top Preis-Leistung</b></p><p>Weitere Produkte finden Sie bald direkt verlinkt in unserem Shop.</p>"


def main():
    product = {
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
        "html": generate_html(product)
    }

    out_file = EXPORTS_DIR / "generator_output_v5.json"
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print("GENERATOR_AGENT_V5_OK")
    print("output_file =", out_file)


if __name__ == "__main__":
    main()