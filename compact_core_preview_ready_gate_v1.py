import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def main():
    source = BASE / Path("storage\state_compact_core\compact_core_preview_verification_v1.json")
    if not source.exists():
        payload = {
            "status": "BROKEN",
            "layer": "COMPACT_CORE_PREVIEW_READY_GATE_V1",
            "mode": "PROJECT_SPECIFIC_ONLY",
            "stage": 9,
            "source_exists": False,
            "preview_ready": False,
            "reason": "preview_verification_missing",
            "next_step": "restore_preview_verification_layer"
        }
    else:
        data = json.loads(source.read_text(encoding="utf-8"))
        checks = data.get("checks", {})
        title_ready = bool(checks.get("title_ready"))
        price_ready = bool(checks.get("price_ready"))
        description_ready = bool(checks.get("description_ready"))
        html_ready = bool(checks.get("html_ready"))
        images_ready = bool(checks.get("images_ready"))
        links_ready = bool(checks.get("links_ready"))
        all_ready = title_ready and price_ready and description_ready and html_ready and images_ready and links_ready
        payload = {
            "status": "OK" if all_ready else "BLOCKED",
            "layer": "COMPACT_CORE_PREVIEW_READY_GATE_V1",
            "mode": "PROJECT_SPECIFIC_ONLY",
            "stage": 9,
            "source_exists": True,
            "source_file": str(source),
            "preview_ready": all_ready,
            "gate_checks": {
                "title_ready": title_ready,
                "price_ready": price_ready,
                "description_ready": description_ready,
                "html_ready": html_ready,
                "images_ready": images_ready,
                "links_ready": links_ready
            },
            "next_step": "preview_ready_for_next_compact_core_layer" if all_ready else "preview_not_ready_stop_here"
        }

    out_path = BASE / Path("storage\state_compact_core\compact_core_preview_ready_gate_v1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("COMPACT_CORE_PREVIEW_READY_GATE_V1_AUDIT")
    print("status =", payload["status"])
    print("layer =", payload["layer"])
    print("mode =", payload["mode"])
    print("stage =", payload["stage"])
    print("source_exists =", payload["source_exists"])
    print("preview_ready =", payload["preview_ready"])
    if payload["source_exists"] and "gate_checks" in payload:
        print("title_ready =", payload["gate_checks"]["title_ready"])
        print("price_ready =", payload["gate_checks"]["price_ready"])
        print("description_ready =", payload["gate_checks"]["description_ready"])
        print("html_ready =", payload["gate_checks"]["html_ready"])
        print("images_ready =", payload["gate_checks"]["images_ready"])
        print("links_ready =", payload["gate_checks"]["links_ready"])
    print("output_file =", str(out_path))

if __name__ == "__main__":
    main()
