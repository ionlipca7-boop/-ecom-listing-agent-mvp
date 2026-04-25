import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def load_json(rel_path):
    p = BASE / rel_path
    if not p.exists():
        return {}, str(p), False
    return json.loads(p.read_text(encoding="utf-8")), str(p), True

def main():
    bridge_data, bridge_path, bridge_exists = load_json(Path("storage\state_compact_core\compact_core_execution_bridge_v1.json"))
    hub_data, hub_path, hub_exists = load_json(Path("storage\state_compact_core\compact_core_state_hub_v1.json"))
    root_data, root_path, root_exists = load_json(Path("storage\state_compact_core\compact_core_transition_front_v1.json"))

    execution_input = bridge_data.get("execution_input", {})
    links = bridge_data.get("links", {})
    generator_output = hub_data.get("generator_output", {})
    front_input = root_data.get("input", {})

    preview_contract = {
        "status": "OK",
        "layer": "COMPACT_CORE_PREVIEW_CONTRACT_V1",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "stage": 9,
        "front_exists": root_exists,
        "hub_exists": hub_exists,
        "bridge_exists": bridge_exists,
        "sources": {
            "transition_front": root_path,
            "state_hub": hub_path,
            "execution_bridge": bridge_path
        },
        "preview_contract": {
            "title": generator_output.get("main_title") or execution_input.get("title") or front_input.get("title") or "",
            "price": generator_output.get("price", execution_input.get("price", "")),
            "description": generator_output.get("description") or execution_input.get("description") or "",
            "html": generator_output.get("html") or execution_input.get("html") or "",
            "category": generator_output.get("category") or execution_input.get("category") or front_input.get("category") or "",
            "images": generator_output.get("images", execution_input.get("images", [])),
            "links": links
        },
        "next_step": "preview_contract_ready_for_stage9_verification"
    }

    out_path = BASE / Path("storage\state_compact_core\compact_core_preview_contract_v1.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(preview_contract, ensure_ascii=False, indent=2), encoding="utf-8")

    print("COMPACT_CORE_PREVIEW_CONTRACT_V1_AUDIT")
    print("status =", preview_contract["status"])
    print("layer =", preview_contract["layer"])
    print("mode =", preview_contract["mode"])
    print("stage =", preview_contract["stage"])
    print("front_exists =", preview_contract["front_exists"])
    print("hub_exists =", preview_contract["hub_exists"])
    print("bridge_exists =", preview_contract["bridge_exists"])
    print("title_ready =", bool(preview_contract["preview_contract"]["title"]))
    print("price_ready =", preview_contract["preview_contract"]["price"] != "")
    print("description_ready =", bool(preview_contract["preview_contract"]["description"]))
    print("html_ready =", bool(preview_contract["preview_contract"]["html"]))
    print("images_count =", len(preview_contract["preview_contract"]["images"]))
    print("output_file =", str(out_path))

if __name__ == "__main__":
    main()
