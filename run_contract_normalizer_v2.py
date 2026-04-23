import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "generator_output_v4_title_recovered.json"
OUT = BASE_DIR / "storage" / "exports" / "generator_output_contract_v2.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "contract_normalizer_v2_2026_04_18.json"

def as_list(value):
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]

def main():
    raw = json.loads(SRC.read_text(encoding="utf-8"))
    normalized = {
        "title": str(raw.get("title") or raw.get("main_title") or "").strip(),
        "main_title": str(raw.get("main_title") or raw.get("title") or "").strip(),
        "titles": as_list(raw.get("titles")),
        "price": raw.get("price"),
        "description": str(raw.get("description") or "").strip(),
        "html": str(raw.get("html") or "").strip(),
        "category": raw.get("category"),
        "images": as_list(raw.get("images")),
        "status": "normalized",
        "contract_version": "v2"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
    archive = {
        "date": "2026-04-18",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "status": "OK",
        "decision": "contract_normalizer_v2_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "normalized_file": str(OUT.relative_to(BASE_DIR)).replace("/", "\\"),
        "contract_version": "v2",
        "required_keys": ["title","main_title","titles","price","description","html","category","images","status","contract_version"],
        "next_step": "build_downstream_probe_v1_against_contract_v2"
    }
    ARCH.write_text(json.dumps(archive, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CONTRACT_NORMALIZER_V2_AUDIT")
    print("status = OK")
    print("decision = contract_normalizer_v2_completed")
    print("normalized_file =", str(OUT.relative_to(BASE_DIR)).replace("/", "\\"))
    print("contract_version =", normalized["contract_version"])
    print("has_title =", "title" in normalized and bool(normalized["title"]))
    print("has_description =", "description" in normalized and bool(normalized["description"]))
    print("has_price =", "price" in normalized and normalized["price"] is not None)
    print("images_is_list =", isinstance(normalized["images"], list))
    print("titles_is_list =", isinstance(normalized["titles"], list))
    print("next_step = build_downstream_probe_v1_against_contract_v2")

if __name__ == "__main__":
    main()
