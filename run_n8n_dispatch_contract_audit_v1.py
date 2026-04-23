import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatch_contract_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatch_contract_v1_audit.txt")
lines = [
    "N8N_DISPATCH_CONTRACT_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "contract_version = " + str(d.get("contract_version")),
    "dispatch_order_count = " + str(len(d.get("dispatch_order", []))),
    "required_input_count = " + str(len(d.get("input_contract", {}).get("required_inputs", []))),
    "required_output_count = " + str(len(d.get("output_contract", {}).get("required_outputs", []))),
    "forbidden_behavior_count = " + str(len(d.get("forbidden_behavior", []))),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "n8n_ready = " + str(d.get("n8n_ready")),
    "contract_ready = " + str(d.get("contract_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
