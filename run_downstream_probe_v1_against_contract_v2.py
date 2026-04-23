import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "generator_output_contract_v2.json"
OUT = BASE_DIR / "storage" / "exports" / "downstream_probe_v1_contract_v2.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "downstream_probe_v1_contract_v2_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    title = str(data.get("title") or "").strip()
    description = str(data.get("description") or "").strip()
    price = data.get("price")
    html = str(data.get("html") or "").strip()
    images = data.get("images") if isinstance(data.get("images"), list) else []
    titles = data.get("titles") if isinstance(data.get("titles"), list) else []
    probe = {
        "status": "OK",
        "decision": "downstream_probe_v1_against_contract_v2_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "contract_version": data.get("contract_version"),
        "title": title,
        "title_length": len(title),
        "description_present": bool(description),
        "price_present": price is not None,
        "html_present": bool(html),
        "images_count": len(images),
        "titles_count": len(titles),
        "ready_for_downstream": bool(title) and bool(description) and price is not None,
        "next_step": "promote_contract_v2_as_downstream_input"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    print("DOWNSTREAM_PROBE_V1_CONTRACT_V2_AUDIT")
    print("status = OK")
    print("decision = downstream_probe_v1_against_contract_v2_completed")
    print("contract_version =", probe["contract_version"])
    print("title_length =", probe["title_length"])
    print("description_present =", probe["description_present"])
    print("price_present =", probe["price_present"])
    print("html_present =", probe["html_present"])
    print("titles_count =", probe["titles_count"])
    print("images_count =", probe["images_count"])
    print("ready_for_downstream =", probe["ready_for_downstream"])
    print("next_step =", probe["next_step"])

if __name__ == "__main__":
    main()
