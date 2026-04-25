import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "inventory_full_payload_mapper_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "real_inventory_api_probe_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "real_inventory_api_probe_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    payload = data.get("inventory_full_payload", {}) if isinstance(data.get("inventory_full_payload"), dict) else {}
    title = str(payload.get("title") or "").strip()
    description = str(payload.get("description") or "").strip()
    html = str(payload.get("html") or "").strip()
    images = payload.get("images") if isinstance(payload.get("images"), list) else []
    category = payload.get("category")
    probe = {
        "status": "OK",
        "decision": "real_inventory_api_probe_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "real_inventory_api_probe_version": "v1",
        "inventory_api_payload_preview": {
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
        "ready_for_real_inventory_api_call": bool(title) and bool(description) and bool(images),
        "next_step": "choose_real_inventory_read_or_real_inventory_update_path"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REAL_INVENTORY_API_PROBE_V1_AUDIT")
    print("status = OK")
    print("decision = real_inventory_api_probe_v1_completed")
    print("real_inventory_api_probe_version =", probe["real_inventory_api_probe_version"])
    print("title_present =", probe["probe_checks"]["title_present"])
    print("description_present =", probe["probe_checks"]["description_present"])
    print("html_present =", probe["probe_checks"]["html_present"])
    print("images_present =", probe["probe_checks"]["images_present"])
    print("category_present =", probe["probe_checks"]["category_present"])
    print("ready_for_real_inventory_api_call =", probe["ready_for_real_inventory_api_call"])
    print("next_step =", probe["next_step"])

if __name__ == "__main__":
    main()
