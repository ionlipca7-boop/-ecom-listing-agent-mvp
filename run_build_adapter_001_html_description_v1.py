import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "new_product_adapter_001.json"
OUT_FILE = BASE_DIR / "storage" / "exports" / "adapter_001_html_description_v1.json"

def main():
    product = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    title = product.get("title") or product.get("main_title") or "USB-C OTG Adapter USB 3.0 Typ-C auf USB-A"
    color = product.get("color") or "Schwarz / Orange / Grau je nach Ausfuehrung"
    plain_text = "Kompakter USB-C OTG Adapter fuer schnelle Datenuebertragung und alltagstaugliche Verbindung von USB-C auf USB-A. Ideal fuer Smartphone, Tablet, Laptop und Zubehoer im Alltag, Buero oder auf Reisen."
    data = {
        "status": "OK",
        "decision": "adapter_001_html_description_built",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "product_key": "adapter_001",
        "title": title,
        "plain_text": plain_text,
        "html": html,
        "sections": ["Einleitung", "Vorteile", "Kompatibilitaet", "Produktdetails", "Hinweise", "Lieferumfang", "Versand"]
    }
    OUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_HTML_OK")
    print("product_key =", data["product_key"])
    print("decision =", data["decision"])
    print("sections_count =", len(data["sections"]))

if __name__ == "__main__":
    main()
