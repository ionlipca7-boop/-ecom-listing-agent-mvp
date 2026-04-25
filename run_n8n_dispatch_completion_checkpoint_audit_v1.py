import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatch_completion_checkpoint_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
chain = d.get("dispatcher_chain_status", {})
ready_count = sum(1 for v in chain.values() if v is True)
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatch_completion_checkpoint_v1_audit.txt")
lines = [
    "N8N_DISPATCH_COMPLETION_CHECKPOINT_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "completion_checkpoint_version = " + str(d.get("completion_checkpoint_version")),
    "dispatcher_ready_component_count = " + str(ready_count),
    "chain_closed = " + str(d.get("chain_closed")),
    "n8n_ready = " + str(d.get("n8n_ready")),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "final_decision = " + str(d.get("final_decision")),
    "dispatcher_completion_ready = " + str(d.get("dispatcher_completion_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
