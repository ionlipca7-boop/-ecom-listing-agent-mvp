import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def main():
    source = BASE / Path("storage\state_compact_core\compact_core_preview_contract_v1.json")
    if not source.exists():
        payload = {
            "status": "BROKEN",
            "layer": "COMPACT_CORE_PREVIEW_VERIFICATION_V1",
            "mode": "PROJECT_SPECIFIC_ONLY",
            "stage": 9,
            "source_exists": False,
            "reason": "preview_contract_json_missing",
            "next_step": "restore_preview_contract_json"
        }
    else:
        data = json.loads(source.read_text(encoding="utf-8"))
        preview = data.get("preview_contract", {})
        title = preview.get("title", "")
        price = preview.get("price", "")
        description = preview.get("description", "")
        html = preview.get("html", "")
        images = preview.get("images", [])
        links = preview.get("links", {})
        payload = {
            "status": "OK",
            "layer": "COMPACT_CORE_PREVIEW_VERIFICATION_V1",
            "mode": "PROJECT_SPECIFIC_ONLY",
            "stage": 9,
            "source_exists": True,
            "source_file": str(source),
            "checks": {
                "title_ready": bool(title),
                "price_ready": price != "",
                "description_ready": bool(description),
                "html_ready": bool(html),
                "images_ready": isinstance(images, list) and len(images) > 0,
                "links_ready": isinstance(links, dict)
            },
            "summary": {
                "title_length": len(title),
                "description_length": len(description),
                "html_length": len(html),
                "images_count": len(images)
            },
            "next_step": "preview_verified_ready_for_next_compact_core_layer"
        }

    out_path = BASE / Path("storage\state_compact_core\compact_core_preview_verification_v1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("COMPACT_CORE_PREVIEW_VERIFICATION_V1_AUDIT")
    print("status =", payload["status"])
    print("layer =", payload["layer"])
    print("mode =", payload["mode"])
    print("stage =", payload["stage"])
    print("source_exists =", payload["source_exists"])
    if payload["status"] == "OK":
        print("title_ready =", payload["checks"]["title_ready"])
        print("price_ready =", payload["checks"]["price_ready"])
        print("description_ready =", payload["checks"]["description_ready"])
        print("html_ready =", payload["checks"]["html_ready"])
        print("images_ready =", payload["checks"]["images_ready"])
        print("links_ready =", payload["checks"]["links_ready"])
        print("images_count =", payload["summary"]["images_count"])
    print("output_file =", str(out_path))

if __name__ == "__main__":
    main()
