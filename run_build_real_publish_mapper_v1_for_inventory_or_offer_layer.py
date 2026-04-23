import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "real_publish_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "real_publish_mapper_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "real_publish_mapper_v1_2026_04_18.json"

def main():
    probe = json.loads(SRC.read_text(encoding="utf-8"))
    preview = probe.get("publish_payload_preview", {}) if isinstance(probe.get("publish_payload_preview"), dict) else {}
    title = str(preview.get("title") or "").strip()
    description = str(preview.get("description") or "").strip()
    html = str(preview.get("html") or "").strip()
    price = preview.get("price")
    category = preview.get("category")
    images = preview.get("images") if isinstance(preview.get("images"), list) else []
    mapped = {
        "status": "OK",
        "decision": "real_publish_mapper_v1_built_for_inventory_or_offer_layer",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "real_publish_mapper_version": "v1",
        "inventory_candidate": {
            "title": title,
            "description": description,
            "html": html,
            "images": images,
            "category": category
        },
        "offer_candidate": {
            "price": price,
            "category": category
        },
        "mapping_checks": {
            "title_present": bool(title),
            "description_present": bool(description),
            "html_present": bool(html),
            "price_present": price is not None,
            "category_present": category is not None and str(category).strip() != "",
            "images_present": bool(images)
        },
        "ready_for_inventory_layer": bool(title) and bool(description) and bool(images),
        "ready_for_offer_layer": price is not None and category is not None and str(category).strip() != "",
        "next_step": "choose_inventory_first_or_offer_first_real_api_probe"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REAL_PUBLISH_MAPPER_V1_AUDIT")
    print("status = OK")
    print("decision = real_publish_mapper_v1_built_for_inventory_or_offer_layer")
    print("real_publish_mapper_version =", mapped["real_publish_mapper_version"])
    print("title_present =", mapped["mapping_checks"]["title_present"])
    print("description_present =", mapped["mapping_checks"]["description_present"])
    print("html_present =", mapped["mapping_checks"]["html_present"])
    print("price_present =", mapped["mapping_checks"]["price_present"])
    print("category_present =", mapped["mapping_checks"]["category_present"])
    print("images_present =", mapped["mapping_checks"]["images_present"])
    print("ready_for_inventory_layer =", mapped["ready_for_inventory_layer"])
    print("ready_for_offer_layer =", mapped["ready_for_offer_layer"])
    print("next_step =", mapped["next_step"])

if __name__ == "__main__":
    main()
