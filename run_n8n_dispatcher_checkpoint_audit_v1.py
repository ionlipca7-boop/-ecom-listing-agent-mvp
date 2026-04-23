import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatcher_checkpoint_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatcher_checkpoint_v1_audit.txt")
lines = [
    "N8N_DISPATCHER_CHECKPOINT_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "selected_branch = " + str(d.get("selected_branch")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "n8n_real_connection_enabled = " + str(d.get("n8n_real_connection_enabled")),
    "n8n_ready = " + str(d.get("n8n_ready")),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "final_decision = " + str(d.get("final_decision")),
    "dispatcher_checkpoint_ready = " + str(d.get("dispatcher_checkpoint_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
