import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "new_product_adapter_001.json"
OUT_FILE = BASE_DIR / "storage" / "exports" / "adapter_001_html_description_v2.json"

def main():
    product = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    title = product.get("title") or product.get("main_title") or "USB-C OTG Adapter USB 3.0 Typ-C auf USB-A"
    plain_text = "Kompakter USB-C OTG Adapter fuer praktische Verbindung von USB-C auf USB-A. Geeignet fuer viele Alltagsgeraete, Reisen und den schnellen Einsatz zu Hause oder im Buero."
    html = \"\"\"<div style='font-family:Arial,sans-serif;font-size:14px;line-height:1.6;color:#222;'>\n<h2 style='font-size:20px;margin:0 0 12px 0;'>USB-C OTG Adapter USB 3.0 Typ-C auf USB-A</h2>\n<p style='margin:0 0 14px 0;'>Kompakter Adapter fuer die praktische Verbindung von USB-C auf USB-A. Ideal fuer Alltag, Reise, Buero und mobile Nutzung.</p>\n<h3 style='font-size:16px;margin:18px 0 8px 0;'>Vorteile</h3>\n<ul style='margin:0 0 14px 18px;padding:0;'>\n<li>Kompakt und leicht mitzunehmen</li>\n<li>USB-C auf USB-A Verbindung fuer viele Geraete</li>\n<li>Geeignet fuer Datentransfer und Ladeanwendungen je nach Endgeraet</li>\n<li>Einfache Nutzung ohne komplizierte Einrichtung</li>\n</ul>\n<h3 style='font-size:16px;margin:18px 0 8px 0;'>Produktdetails</h3>\n<ul style='margin:0 0 14px 18px;padding:0;'>\n<li>Produktart: USB-C OTG Adapter</li>\n<li>Anschluss A: USB-C</li>\n<li>Anschluss B: USB-A</li>\n<li>Zustand: Neu</li>\n<li>Marke: No-Name / ohne Markenaufdruck je nach Charge</li>\n</ul>\n<h3 style='font-size:16px;margin:18px 0 8px 0;'>Hinweise</h3>\n<ul style='margin:0 0 14px 18px;padding:0;'>\n<li>Bitte Anschluesse Ihres Geraets vor dem Kauf vergleichen.</li>\n<li>Farbton und kleine Designdetails koennen je nach Charge leicht abweichen.</li>\n</ul>\n<h3 style='font-size:16px;margin:18px 0 8px 0;'>Lieferumfang</h3>\n<p style='margin:0 0 14px 0;'>1x USB-C OTG Adapter</p>\n<h3 style='font-size:16px;margin:18px 0 8px 0;'>Versand</h3>\n<p style='margin:0;'>Versand aus Deutschland. Die konkrete Versandart richtet sich nach effizienter und sicherer Zustellung.</p>\n</div>\"\"\"
    data = {
        "status": "OK",
        "decision": "adapter_001_html_description_built_v2",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "product_key": "adapter_001",
        "title": title,
        "plain_text": plain_text,
        "html": html,
        "sections": ["Einleitung","Vorteile","Produktdetails","Hinweise","Lieferumfang","Versand"]
    }
    OUT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_HTML_V2_OK")
    print("product_key =", data["product_key"])
    print("decision =", data["decision"])
    print("sections_count =", len(data["sections"]))

if __name__ == "__main__":
    main()
