import json
from pathlib import Path
from datetime import datetime, UTC

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    product_key = "adapter_001"
    title = "USB-C OTG Adapter USB 3.0 Typ-C auf USB-A Schnellladen Daten"

    html_parts = []
    html_parts.append(f"^<h2^>{title}^</h2^>")
    html_parts.append("^<p^>Kompakter USB-C auf USB-A Adapter fur schnelles Laden und Datenubertragung.^</p^>")
    html_parts.append("^<ul^>")
    html_parts.append("^<li^>USB-C auf USB-A OTG Funktion^</li^>")
    html_parts.append("^<li^>USB 3.0 schnelle Datenubertragung^</li^>")
    html_parts.append("^<li^>Kompakt und leicht^</li^>")
    html_parts.append("^<li^>Ideal fur Smartphone, Tablet, Laptop^</li^>")
    html_parts.append("^</ul^>")
    html_parts.append("^<p^>? Schneller Versand^<br^>? Top Qualitat^<br^>? Perfekt fur Alltag und Reisen^</p^>")

    html = "".join(html_parts)

    output = {
        "status": "OK",
        "decision": "html_description_generated",
        "product_key": product_key,
        "title": title,
        "html": html,
        "generated_at_utc": datetime.now(UTC).isoformat()
    }

    path = EXPORTS_DIR / "adapter_001_html_description_v1.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("HTML_GENERATED")
    print("file =", path)

if __name__ == "__main__":
    main()
