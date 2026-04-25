import json
from pathlib import Path
from datetime import datetime, UTC

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "adapter_001_html_description_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "adapter_001_html_description_clean_v1.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    html = data.get("html", "")
    html = html.replace("^<", "<").replace("^>", ">")
    html = html.replace("? Schneller Versand", "Schneller Versand")
    html = html.replace("? Top Qualitat", "Top Qualitaet")
    html = html.replace("? Perfekt fur Alltag und Reisen", "Perfekt fuer Alltag und Reisen")
    html = html.replace("fur", "fuer")
    html = html.replace("Datenubertragung", "Datenuebertragung")
    data["status"] = "OK"
    data["decision"] = "html_description_cleaned"
    data["html"] = html
    data["cleaned_at_utc"] = datetime.now(UTC).isoformat()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("HTML_CLEAN_OK")
    print("file =", OUT)

if __name__ == "__main__":
    main()
