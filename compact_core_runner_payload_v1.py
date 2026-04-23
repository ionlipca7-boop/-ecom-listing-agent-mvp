import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def main():
    gate_file = BASE / Path("storage\state_compact_core\compact_core_preview_ready_gate_v1.json")
    preview_file = BASE / Path("storage\state_compact_core\compact_core_preview_contract_v1.json")
    payload = {}
    payload["layer"] = "COMPACT_CORE_RUNNER_PAYLOAD_V1"
    payload["mode"] = "PROJECT_SPECIFIC_ONLY"
    payload["stage"] = 9

    if not gate_file.exists():
        payload["status"] = "BROKEN"
        payload["gate_exists"] = False
        payload["preview_exists"] = preview_file.exists()
        payload["runner_payload_ready"] = False
        payload["reason"] = "preview_ready_gate_missing"
        payload["next_step"] = "restore_preview_ready_gate_v1"

    elif not preview_file.exists():
        payload["status"] = "BROKEN"
        payload["gate_exists"] = True
        payload["preview_exists"] = False
        payload["runner_payload_ready"] = False
        payload["reason"] = "preview_contract_missing"
        payload["next_step"] = "restore_preview_contract_v1"

    else:
        gate_data = json.loads(gate_file.read_text(encoding="utf-8"))
        preview_data = json.loads(preview_file.read_text(encoding="utf-8"))
        preview_ready = bool(gate_data.get("preview_ready"))
        preview = preview_data.get("preview_contract", {})
        title = preview.get("title", "")
        price = preview.get("price", "")
        description = preview.get("description", "")
        html = preview.get("html", "")
        category = preview.get("category", "")
        images = preview.get("images", [])
        links = preview.get("links", {})
        ready = preview_ready and bool(title) and bool(str(price)) and bool(description) and bool(html) and bool(images)
        if ready:
            payload["status"] = "OK"
            payload["next_step"] = "runner_payload_ready_for_next_compact_core_layer"
        else:
            payload["status"] = "BLOCKED"
            payload["next_step"] = "runner_payload_blocked_stop_here"
        payload["gate_exists"] = True
        payload["preview_exists"] = True
        payload["preview_ready"] = preview_ready
        payload["runner_payload_ready"] = ready
        payload["runner_payload"] = {}
        payload["runner_payload"]["title"] = title
        payload["runner_payload"]["price"] = price
        payload["runner_payload"]["description"] = description
        payload["runner_payload"]["html"] = html
        payload["runner_payload"]["category"] = category
        payload["runner_payload"]["images"] = images
        payload["runner_payload"]["links"] = links
        payload["summary"] = {}
        payload["summary"]["title_length"] = len(title)
        payload["summary"]["description_length"] = len(description)
        payload["summary"]["html_length"] = len(html)
        payload["summary"]["images_count"] = len(images)

    out_file = BASE / Path("storage\state_compact_core\compact_core_runner_payload_v1.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("COMPACT_CORE_RUNNER_PAYLOAD_V1_AUDIT")
    print("status =", payload["status"])
    print("layer =", payload["layer"])
    print("mode =", payload["mode"])
    print("stage =", payload["stage"])
    print("gate_exists =", payload["gate_exists"])
    print("preview_exists =", payload["preview_exists"])
    if "preview_ready" in payload:
        print("preview_ready =", payload["preview_ready"])
    print("runner_payload_ready =", payload["runner_payload_ready"])
    if "summary" in payload:
        print("images_count =", payload["summary"]["images_count"])
    print("output_file =", str(out_file))

if __name__ == "__main__":
    main()
