import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "downstream_input_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "publish_payload_probe_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "publish_payload_probe_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    title = str(data.get("title") or "").strip()
    description = str(data.get("description") or "").strip()
    html = str(data.get("html") or "").strip()
    price = data.get("price")
    category = data.get("category")
    images = data.get("images") if isinstance(data.get("images"), list) else []
    payload = {
        "status": "OK",
        "decision": "publish_payload_probe_v1_fixed_and_rebuilt",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "payload": {
            "title": title,
            "description": description,
            "html": html,
            "price": price,
            "category": category,
            "images": images
        },
        "payload_checks": {
            "title_present": bool(title),
            "description_present": bool(description),
            "html_present": bool(html),
            "price_present": price is not None,
            "category_present": category is not None and str(category).strip() != "",
            "images_present": bool(images)
        },
        "ready_for_publish_layer": bool(title) and bool(description) and price is not None,
        "next_step": "build_publish_payload_mapper_v1_or_real_publish_probe_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PUBLISH_PAYLOAD_PROBE_V1_FIX_AUDIT")
    print("status = OK")
    print("decision = publish_payload_probe_v1_fixed_and_rebuilt")
    print("title_present =", payload["payload_checks"]["title_present"])
    print("description_present =", payload["payload_checks"]["description_present"])
    print("html_present =", payload["payload_checks"]["html_present"])
    print("price_present =", payload["payload_checks"]["price_present"])
    print("category_present =", payload["payload_checks"]["category_present"])
    print("images_present =", payload["payload_checks"]["images_present"])
    print("ready_for_publish_layer =", payload["ready_for_publish_layer"])
    print("next_step =", payload["next_step"])

if __name__ == "__main__":
    main()
