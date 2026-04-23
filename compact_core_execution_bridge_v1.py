import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def load_json(rel_path):
    p = BASE / rel_path
    if not p.exists():
        return {}, str(p), False
    return json.loads(p.read_text(encoding="utf-8")), str(p), True

def main():
    hub_data, hub_path, hub_exists = load_json(Path("storage/state_compact_core/compact_core_state_hub_v1.json"))
    root_data, root_path, root_exists = load_json(Path("storage/state_compact_core/compact_core_transition_front_v1.json"))
    gen_data, gen_path, gen_exists = load_json(Path("storage/exports/generator_output_v4.json"))

    foundation = hub_data.get("foundation", {})
    agents = hub_data.get("agents", {})
    generator_output = hub_data.get("generator_output", {})

    manifest_ready = foundation.get("manifest_ready") is True
    rules_ready = foundation.get("rules_ready") is True
    state_ready = foundation.get("state_ready") is True
    history_ready = foundation.get("history_ready") is True
    control_ready = agents.get("control_ready") is True
    runner_ready = agents.get("runner_ready") is True
    archivist_ready = agents.get("archivist_ready") is True

    title_ready = generator_output.get("title_ready") is True
    description_ready = generator_output.get("description_ready") is True
    html_ready = generator_output.get("html_ready") is True
    images_ready = generator_output.get("images_ready") is True
    price_ready = generator_output.get("price_ready") is True
    output_ready = all([title_ready, description_ready, html_ready, images_ready, price_ready])

    execution_input = {
        "title": gen_data.get("main_title") or gen_data.get("title"),
        "description": gen_data.get("description"),
        "html": gen_data.get("html"),
        "images": gen_data.get("images", []),
        "price": gen_data.get("price"),
        "category": gen_data.get("category")
    }

    bridge_ready = all([hub_exists, root_exists, gen_exists, manifest_ready, rules_ready, state_ready, history_ready, control_ready, runner_ready, archivist_ready, output_ready])

    bridge = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "layer": "COMPACT_CORE_EXECUTION_BRIDGE_V1",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "stage": 9,
        "root_role": "compact_execution_bridge",
        "hub_connected": hub_exists,
        "root_connected": root_exists,
        "generator_source_connected": gen_exists,
        "bridge_ready": bridge_ready,
        "execution_mode": "PREVIEW_ONLY_NO_LIVE",
        "execution_target": "runner_preview_path",
        "execution_input": execution_input,
        "links": {
            "control_to_runner": control_ready and runner_ready,
            "runner_to_generator": runner_ready and gen_exists,
            "generator_to_output": output_ready
        },
        "next_step": "build_compact_core_preview_contract_v1",
        "note": "compact execution bridge created without live execution"
    }

    out_json = BASE / "storage/state_compact_core/compact_core_execution_bridge_v1.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(bridge, ensure_ascii=False, indent=2), encoding="utf-8")

    out_txt = BASE / "storage/audit/compact_core_execution_bridge_v1_audit.txt"
    out_txt.write_text("COMPACT_CORE_EXECUTION_BRIDGE_V1_AUDIT\nstatus = OK\nstage = 9\nroot_role = compact_execution_bridge\nhub_connected = " + str(hub_exists) + "\nroot_connected = " + str(root_exists) + "\ngenerator_source_connected = " + str(gen_exists) + "\nbridge_ready = " + str(bridge_ready) + "\nexecution_mode = PREVIEW_ONLY_NO_LIVE\nnext_step = " + bridge["next_step"] + "\n", encoding="utf-8")

    print("COMPACT_CORE_EXECUTION_BRIDGE_V1_FINAL_AUDIT")
    print("status = OK")
    print("stage = 9")
    print("root_role = compact_execution_bridge")
    print("hub_connected =", hub_exists)
    print("root_connected =", root_exists)
    print("generator_source_connected =", gen_exists)
    print("bridge_ready =", bridge_ready)
    print("execution_mode = PREVIEW_ONLY_NO_LIVE")
    print("next_step =", bridge["next_step"])

if __name__ == "__main__":
    main()
