import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatch_audit_flow_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatch_audit_flow_v1_audit.txt")
lines = [
    "N8N_DISPATCH_AUDIT_FLOW_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "audit_flow_version = " + str(d.get("audit_flow_version")),
    "audit_sequence_count = " + str(len(d.get("audit_sequence", []))),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "audit_flow_ready = " + str(d.get("audit_flow_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
