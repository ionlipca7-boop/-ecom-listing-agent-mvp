import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatch_archivist_handoff_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatch_archivist_handoff_v1_audit.txt")
lines = [
    "N8N_DISPATCH_ARCHIVIST_HANDOFF_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "archivist_handoff_version = " + str(d.get("archivist_handoff_version")),
    "handoff_mode = " + str(d.get("handoff_mode")),
    "required_handoff_field_count = " + str(len(d.get("required_handoff_fields", []))),
    "blocked_condition_count = " + str(len(d.get("blocked_conditions", []))),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "archivist_handoff_ready = " + str(d.get("archivist_handoff_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
