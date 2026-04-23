import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "publish_payload_mapper_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "real_publish_probe_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "real_publish_probe_v1_2026_04_18.json"

def main():
    mapper = json.loads(SRC.read_text(encoding="utf-8"))
    listing = mapper.get("listing_data", {}) if isinstance(mapper.get("listing_data"), dict) else {}
    title = str(listing.get("title") or "").strip()
    description = str(listing.get("description") or "").strip()
    html = str(listing.get("html") or "").strip()
    price = listing.get("price")
    category = listing.get("category")
    images = listing.get("images") if isinstance(listing.get("images"), list) else []
    probe = {
        "status": "OK",
        "decision": "real_publish_probe_v1_built_from_publish_mapper",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "real_publish_contract_version": "v1",
        "publish_payload_preview": {
            "title": title,
            "description": description,
            "html": html,
            "price": price,
            "category": category,
            "images": images
        },
        "probe_checks": {
            "title_present": bool(title),
            "description_present": bool(description),
            "html_present": bool(html),
            "price_present": price is not None,
            "category_present": category is not None and str(category).strip() != "",
            "images_present": bool(images)
        },
        "ready_for_api_layer": bool(title) and bool(description) and price is not None and bool(images),
        "next_step": "build_real_publish_mapper_v1_for_inventory_or_offer_layer"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REAL_PUBLISH_PROBE_V1_AUDIT")
    print("status = OK")
    print("decision = real_publish_probe_v1_built_from_publish_mapper")
    print("real_publish_contract_version =", probe["real_publish_contract_version"])
    print("title_present =", probe["probe_checks"]["title_present"])
    print("description_present =", probe["probe_checks"]["description_present"])
    print("html_present =", probe["probe_checks"]["html_present"])
    print("price_present =", probe["probe_checks"]["price_present"])
    print("category_present =", probe["probe_checks"]["category_present"])
    print("images_present =", probe["probe_checks"]["images_present"])
    print("ready_for_api_layer =", probe["ready_for_api_layer"])
    print("next_step =", probe["next_step"])

if __name__ == "__main__":
    main()
