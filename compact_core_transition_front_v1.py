import json
from pathlib import Path

BASE = Path(r"D:\ECOM_LISTING_AGENT_MVP")

def read_json(rel_path):
    p = BASE / rel_path
    if not p.exists():
        return {"exists": False, "path": str(p)}
    try:
        return {"exists": True, "path": str(p), "data": json.loads(p.read_text(encoding="utf-8"))}
    except Exception as e:
        return {"exists": True, "path": str(p), "error": str(e)}

def read_text(rel_path):
    p = BASE / rel_path
    if not p.exists():
        return {"exists": False, "path": str(p)}
    try:
        return {"exists": True, "path": str(p), "text": p.read_text(encoding="utf-8")}
    except Exception as e:
        return {"exists": True, "path": str(p), "error": str(e)}

def detect_generator_source():
    candidates = [
        Path("storage/outputs/generator_output_extended.json"),
        Path("storage/outputs/generator_output.json"),
        Path("storage/exports/generator_output_extended.json"),
        Path("storage/exports/generator_output_v4.json"),
    ]
    for rel in candidates:
        p = BASE / rel
        if p.exists():
            return {"found": True, "path": str(p), "rel": str(rel)}
    return {"found": False, "path": None, "rel": None}

def load_generator_payload(gen_info):
    if not gen_info.get("found"):
        return {"exists": False, "keys": [], "title_ready": False, "description_ready": False, "html_ready": False, "images_ready": False}
    p = Path(gen_info["path"])
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return {"exists": True, "path": str(p), "error": str(e), "keys": [], "title_ready": False, "description_ready": False, "html_ready": False, "images_ready": False}
    keys = list(data.keys()) if isinstance(data, dict) else []
    title_value = data.get("main_title") or data.get("title")
    description_value = data.get("description")
    html_value = data.get("html")
    images_value = data.get("images")
    return {
        "exists": True,
        "path": str(p),
        "keys": keys,
        "title_ready": bool(title_value),
        "description_ready": bool(description_value),
        "html_ready": bool(html_value),
        "images_ready": isinstance(images_value, list),
    }

def main():
    stage_transition = read_json(Path("storage/memory/archive/stage_1_to_8_complete_transition.json"))
    canon_audit = read_json(Path("storage/memory/archive/canon_9_step_audit_v2.json"))
    stage_audit_txt = read_text(Path("storage/audit/stage_1_to_8_complete_audit.txt"))
    generator_source = detect_generator_source()
    generator_payload = load_generator_payload(generator_source)

    foundation_ok = False
    ready_for_stage_9 = False
    if stage_transition.get("exists") and "data" in stage_transition:
        d = stage_transition["data"]
        foundation = d.get("foundation", {})
        agents = d.get("agents", {})
        foundation_ok = all(foundation.get(k) == "OK" for k in ["manifest", "rules", "state", "history"]) and all(agents.get(k) == "OK" for k in ["control_agent", "archivist_agent", "runner_agent"]) and d.get("n8n_orchestration") == "OK"
        ready_for_stage_9 = bool(d.get("ready_for_stage_9"))

    compact_root = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "layer": "COMPACT_CORE_TRANSITION_FRONT_V1",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "stage": 9,
        "root_role": "new_transition_root",
        "old_stages_1_to_8_locked": True,
        "foundation_ok": foundation_ok,
        "ready_for_stage_9": ready_for_stage_9,
        "inputs": {
            "stage_transition_archive": stage_transition.get("path"),
            "canon_9_step_archive": canon_audit.get("path"),
            "stage_1_to_8_audit_txt": stage_audit_txt.get("path"),
            "generator_source": generator_source.get("path")
        },
        "links": {
            "control_ready": foundation_ok,
            "runner_ready": foundation_ok,
            "generator_ready": generator_payload.get("exists", False),
            "output_ready": generator_payload.get("description_ready", False) or generator_payload.get("html_ready", False)
        },
        "generator_snapshot": generator_payload,
        "next_step": "build_compact_core_state_hub_v1",
        "note": "transition root created without replacing old agents or live paths"
    }

    out_json = BASE / "storage/state_compact_core/compact_core_transition_front_v1.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(compact_root, ensure_ascii=False, indent=2), encoding="utf-8")

    out_txt = BASE / "storage/audit/compact_core_transition_front_v1_audit.txt"
    out_txt.write_text(
        "COMPACT_CORE_TRANSITION_FRONT_V1_AUDIT\n" +
        "status = OK\n" +
        "stage = 9\n" +
        "root_role = new_transition_root\n" +
        "foundation_ok = " + str(compact_root["foundation_ok"]) + "\n" +
        "ready_for_stage_9 = " + str(compact_root["ready_for_stage_9"]) + "\n" +
        "generator_ready = " + str(compact_root["links"]["generator_ready"]) + "\n" +
        "output_ready = " + str(compact_root["links"]["output_ready"]) + "\n" +
        "next_step = " + compact_root["next_step"] + "\n",
        encoding="utf-8"
    )

    print("COMPACT_CORE_TRANSITION_FRONT_V1_FINAL_AUDIT")
    print("status = OK")
    print("stage = 9")
    print("root_role = new_transition_root")
    print("foundation_ok =", compact_root["foundation_ok"])
    print("ready_for_stage_9 =", compact_root["ready_for_stage_9"])
    print("generator_ready =", compact_root["links"]["generator_ready"])
    print("output_ready =", compact_root["links"]["output_ready"])
    print("next_step =", compact_root["next_step"])

if __name__ == "__main__":
    main()
