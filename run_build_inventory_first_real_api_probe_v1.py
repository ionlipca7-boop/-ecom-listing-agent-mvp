import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "real_publish_mapper_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "inventory_first_real_api_probe_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "inventory_first_real_api_probe_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    inv = data.get("inventory_candidate", {}) if isinstance(data.get("inventory_candidate"), dict) else {}
    title = str(inv.get("title") or "").strip()
    description = str(inv.get("description") or "").strip()
    html = str(inv.get("html") or "").strip()
    images = inv.get("images") if isinstance(inv.get("images"), list) else []
    category = inv.get("category")
    probe = {
        "status": "OK",
        "decision": "inventory_first_real_api_probe_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "inventory_probe_version": "v1",
        "inventory_payload_preview": {
            "title": title,
            "description": description,
            "html": html,
            "images": images,
            "category": category
        },
        "probe_checks": {
            "title_present": bool(title),
            "description_present": bool(description),
            "html_present": bool(html),
            "images_present": bool(images),
            "category_present": category is not None and str(category).strip() != ""
        },
        "ready_for_inventory_api_mapping": bool(title) and bool(description) and bool(images),
        "next_step": "build_inventory_full_payload_mapper_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    print("INVENTORY_FIRST_REAL_API_PROBE_V1_AUDIT")
    print("status = OK")
    print("decision = inventory_first_real_api_probe_v1_completed")
    print("inventory_probe_version =", probe["inventory_probe_version"])
    print("title_present =", probe["probe_checks"]["title_present"])
    print("description_present =", probe["probe_checks"]["description_present"])
    print("html_present =", probe["probe_checks"]["html_present"])
    print("images_present =", probe["probe_checks"]["images_present"])
    print("category_present =", probe["probe_checks"]["category_present"])
    print("ready_for_inventory_api_mapping =", probe["ready_for_inventory_api_mapping"])
    print("next_step =", probe["next_step"])

if __name__ == "__main__":
    main()
