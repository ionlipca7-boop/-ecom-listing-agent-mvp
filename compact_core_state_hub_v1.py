import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def load_json(rel_path):
    p = BASE / rel_path
    if not p.exists():
        return {}, str(p), False
    return json.loads(p.read_text(encoding="utf-8")), str(p), True

def find_generator():
    candidates = [
        Path("storage/exports/generator_output_v4.json"),
        Path("storage/exports/generator_output_extended.json"),
        Path("storage/outputs/generator_output_extended.json"),
        Path("storage/outputs/generator_output.json")
    ]
    for rel in candidates:
        p = BASE / rel
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8")), str(p), True
    return {}, "", False

def main():
    root_data, root_path, root_exists = load_json(Path("storage/state_compact_core/compact_core_transition_front_v1.json"))
    stage_data, stage_path, stage_exists = load_json(Path("storage/memory/archive/stage_1_to_8_complete_transition.json"))
    canon_data, canon_path, canon_exists = load_json(Path("storage/memory/archive/canon_9_step_audit_v2.json"))
    gen_data, gen_path, gen_exists = find_generator()

    foundation = stage_data.get("foundation", {})
    agents = stage_data.get("agents", {})

    manifest_ready = foundation.get("manifest") == "OK"
    rules_ready = foundation.get("rules") == "OK"
    state_ready = foundation.get("state") == "OK"
    history_ready = foundation.get("history") == "OK"
    control_ready = agents.get("control_agent") == "OK"
    runner_ready = agents.get("runner_agent") == "OK"
    archivist_ready = agents.get("archivist_agent") == "OK"
    n8n_ready = stage_data.get("n8n_orchestration") == "OK"

    generator_ready = gen_exists and isinstance(gen_data, dict) and bool(gen_data)
    title_ready = bool(gen_data.get("main_title") or gen_data.get("title")) if isinstance(gen_data, dict) else False
    description_ready = bool(gen_data.get("description")) if isinstance(gen_data, dict) else False
    html_ready = bool(gen_data.get("html")) if isinstance(gen_data, dict) else False
    images_ready = isinstance(gen_data.get("images"), list) if isinstance(gen_data, dict) else False
    image_count = len(gen_data.get("images")) if images_ready else 0
    price_ready = isinstance(gen_data, dict) and ("price" in gen_data)
    output_ready = description_ready and html_ready

    compact_hub = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "layer": "COMPACT_CORE_STATE_HUB_V1",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "stage": 9,
        "root_role": "compact_state_center",
        "root_front_connected": root_exists,
        "foundation": {"manifest_ready": manifest_ready, "rules_ready": rules_ready, "state_ready": state_ready, "history_ready": history_ready},
        "agents": {"control_ready": control_ready, "runner_ready": runner_ready, "archivist_ready": archivist_ready},
        "orchestration": {"n8n_ready": n8n_ready, "canon_ready_for_stage_9": bool(canon_data.get("ready_for_stage_9"))},
        "generator_output": {"generator_ready": generator_ready, "title_ready": title_ready, "description_ready": description_ready, "html_ready": html_ready, "images_ready": images_ready, "image_count": image_count, "price_ready": price_ready, "source_path": gen_path},
        "transition_root_snapshot": {"root_role": root_data.get("root_role"), "foundation_ok": root_data.get("foundation_ok"), "ready_for_stage_9": root_data.get("ready_for_stage_9")},
        "system_ready": all([manifest_ready, rules_ready, state_ready, history_ready, control_ready, runner_ready, archivist_ready, n8n_ready, generator_ready, title_ready, description_ready, html_ready]),
        "next_step": "build_compact_core_execution_bridge_v1",
        "note": "compact state hub created as central state layer for stage 9"
    }

    out_json = BASE / "storage/state_compact_core/compact_core_state_hub_v1.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(compact_hub, ensure_ascii=False, indent=2), encoding="utf-8")

    out_txt = BASE / "storage/audit/compact_core_state_hub_v1_audit.txt"
    out_txt.write_text("COMPACT_CORE_STATE_HUB_V1_AUDIT\nstatus = OK\nstage = 9\nroot_role = compact_state_center\nroot_front_connected = " + str(root_exists) + "\ncontrol_ready = " + str(control_ready) + "\nrunner_ready = " + str(runner_ready) + "\ngenerator_ready = " + str(generator_ready) + "\noutput_ready = " + str(output_ready) + "\nsystem_ready = " + str(compact_hub["system_ready"]) + "\nnext_step = " + compact_hub["next_step"] + "\n", encoding="utf-8")

    print("COMPACT_CORE_STATE_HUB_V1_FINAL_AUDIT")
    print("status = OK")
    print("stage = 9")
    print("root_role = compact_state_center")
    print("root_front_connected =", root_exists)
    print("control_ready =", control_ready)
    print("runner_ready =", runner_ready)
    print("generator_ready =", generator_ready)
    print("output_ready =", output_ready)
    print("system_ready =", compact_hub["system_ready"])
    print("next_step =", compact_hub["next_step"])

if __name__ == "__main__":
    main()
