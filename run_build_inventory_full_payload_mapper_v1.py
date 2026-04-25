import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "inventory_first_real_api_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "inventory_full_payload_mapper_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "inventory_full_payload_mapper_v1_2026_04_18.json"

def main():
    probe = json.loads(SRC.read_text(encoding="utf-8"))
    preview = probe.get("inventory_payload_preview", {}) if isinstance(probe.get("inventory_payload_preview"), dict) else {}
    title = str(preview.get("title") or "").strip()
    description = str(preview.get("description") or "").strip()
    html = str(preview.get("html") or "").strip()
    images = preview.get("images") if isinstance(preview.get("images"), list) else []
    category = preview.get("category")
    mapped = {
        "status": "OK",
        "decision": "inventory_full_payload_mapper_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "inventory_payload_mapper_version": "v1",
        "inventory_full_payload": {
            "title": title,
            "description": description,
            "html": html,
            "images": images,
            "category": category
        },
        "payload_checks": {
            "title_present": bool(title),
            "description_present": bool(description),
            "html_present": bool(html),
            "images_present": bool(images),
            "category_present": category is not None and str(category).strip() != ""
        },
        "ready_for_real_inventory_api_probe": bool(title) and bool(description) and bool(images),
        "next_step": "build_real_inventory_api_probe_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(mapped, ensure_ascii=False, indent=2), encoding="utf-8")
    print("INVENTORY_FULL_PAYLOAD_MAPPER_V1_AUDIT")
    print("status = OK")
    print("decision = inventory_full_payload_mapper_v1_completed")
    print("inventory_payload_mapper_version =", mapped["inventory_payload_mapper_version"])
    print("title_present =", mapped["payload_checks"]["title_present"])
    print("description_present =", mapped["payload_checks"]["description_present"])
    print("html_present =", mapped["payload_checks"]["html_present"])
    print("images_present =", mapped["payload_checks"]["images_present"])
    print("category_present =", mapped["payload_checks"]["category_present"])
    print("ready_for_real_inventory_api_probe =", mapped["ready_for_real_inventory_api_probe"])
    print("next_step =", mapped["next_step"])

if __name__ == "__main__":
    main()
