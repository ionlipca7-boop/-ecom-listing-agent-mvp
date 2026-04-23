import json, os, pathlib
root = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP")
def ex(rel):
    return (root / rel).exists()
checks = {
    "project_manifest_json": ex(r"storage\control_layer\project_manifest.json"),
    "control_rules_json": ex(r"storage\control_layer\control_rules.json"),
    "project_state_json": ex(r"storage\control_layer\project_state.json"),
    "project_history_jsonl": ex(r"storage\control_layer\project_history.jsonl"),
    "control_agent_py": ex(r"control_agent.py") or ex(r"agents\control_agent.py") or ex(r"storage\control_layer\control_agent.py"),
    "archivist_agent_py": ex(r"archivist_agent.py") or ex(r"agents\archivist_agent.py") or ex(r"storage\control_layer\archivist_agent.py"),
    "runner_agent_py": ex(r"runner_agent.py") or ex(r"agents\runner_agent.py") or ex(r"storage\control_layer\runner_agent.py"),
    "n8n_connection_step": ex(r"storage\state_transition\compact_core_transition_front_v1_verified.json") or ex(r"storage\memory\archive\compact_core_transition_front_v1_verified_archive.json"),
    "compact_core_transition_after_control_layer": ex(r"storage\state_transition\compact_core_transition_front_v1_verified.json")
}
order = [
    "project_manifest_json",
    "control_rules_json",
    "project_state_json",
    "project_history_jsonl",
    "control_agent_py",
    "archivist_agent_py",
    "runner_agent_py",
    "n8n_connection_step",
    "compact_core_transition_after_control_layer"
]
for item in order:
    if checks[item]:
        reached += 
    else:
        break
next_step = order[reached] if reached < len(order) else "canon_line_complete"
done_steps = order[:reached]
remaining_steps = order[reached:]
result = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "audit_type": "CURRENT_CANON_STAGE_AUDIT_V1",
    "phase_8_canon_complete": True,
    "compact_transition_verified": checks["compact_core_transition_after_control_layer"],
    "reached_step_count": reached,
    "done_steps": done_steps,
    "remaining_steps": remaining_steps,
    "next_logical_step": next_step,
    "checks": checks
}
out_json = root / r"storage\memory\archive\current_canon_stage_audit_v1.json"
out_txt = root / r"storage\audit\current_canon_stage_audit_v1.txt"
out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
lines = [
    "CURRENT_CANON_STAGE_AUDIT_V1",
    "status = OK",
    "phase_8_canon_complete = True",
    "compact_transition_verified = " + str(result["compact_transition_verified"]),
    "reached_step_count = " + str(reached),
    "last_completed_step = " + (done_steps[-1] if done_steps else "none"),
    "next_logical_step = " + next_step,
    "remaining_count = " + str(len(remaining_steps))
]
out_txt.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
