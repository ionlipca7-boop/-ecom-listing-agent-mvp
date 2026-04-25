import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatch_decision_gate_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatch_decision_gate_v1_audit.txt")
lines = [
    "N8N_DISPATCH_DECISION_GATE_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "decision_gate_version = " + str(d.get("decision_gate_version")),
    "decision_source_required = " + str(d.get("decision_source_required")),
    "stop_condition_count = " + str(len(d.get("stop_conditions", []))),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "decision_gate_ready = " + str(d.get("decision_gate_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
