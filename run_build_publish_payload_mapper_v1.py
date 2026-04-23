import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "publish_payload_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "publish_payload_mapper_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "publish_payload_mapper_v1_2026_04_18.json"

def main():
    probe = json.loads(SRC.read_text(encoding="utf-8"))
    payload = probe.get("payload", {}) if isinstance(probe.get("payload"), dict) else {}
    title = str(payload.get("title") or "").strip()
    description = str(payload.get("description") or "").strip()
    html = str(payload.get("html") or "").strip()
    price = payload.get("price")
    category = payload.get("category")
    images = payload.get("images") if isinstance(payload.get("images"), list) else []
    mapped = {
        "status": "OK",
        "decision": "publish_payload_mapper_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "publish_contract_version": "v1",
        "listing_data": {
            "title": title,
            "description": description,
            "html": html,
            "price": price,
            "category": category,
            "images": images
        },
        "mapping_checks": {
            "title_present": bool(title),
            "description_present": bool(description),
            "html_present": bool(html),
            "price_present": price is not None,
            "category_present": category is not None and str(category).strip() != "",
            "images_present": bool(images)
        },
        "ready_for_real_publish_probe": bool(title) and bool(description) and price is not None and bool(images),
        "next_step": "build_real_publish_probe_v1_from_publish_mapper"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PUBLISH_PAYLOAD_MAPPER_V1_AUDIT")
    print("status = OK")
    print("decision = publish_payload_mapper_v1_completed")
    print("publish_contract_version =", mapped["publish_contract_version"])
    print("title_present =", mapped["mapping_checks"]["title_present"])
    print("description_present =", mapped["mapping_checks"]["description_present"])
    print("html_present =", mapped["mapping_checks"]["html_present"])
    print("price_present =", mapped["mapping_checks"]["price_present"])
    print("category_present =", mapped["mapping_checks"]["category_present"])
    print("images_present =", mapped["mapping_checks"]["images_present"])
    print("ready_for_real_publish_probe =", mapped["ready_for_real_publish_probe"])
    print("next_step =", mapped["next_step"])

if __name__ == "__main__":
    main()
