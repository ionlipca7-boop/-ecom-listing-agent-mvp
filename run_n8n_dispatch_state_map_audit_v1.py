import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatch_state_map_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatch_state_map_v1_audit.txt")
lines = [
    "N8N_DISPATCH_STATE_MAP_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "state_map_version = " + str(d.get("state_map_version")),
    "entry_state = " + str(d.get("entry_state")),
    "allowed_transition_count = " + str(len(d.get("allowed_state_transitions", []))),
    "current_state_confirmed = " + str(d.get("current_state_confirmed")),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "state_map_ready = " + str(d.get("state_map_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
