import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\n8n_dispatch_payload_contract_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\n8n_dispatch_payload_contract_v1_audit.txt")
lines = [
    "N8N_DISPATCH_PAYLOAD_CONTRACT_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "dispatcher_role = " + str(d.get("dispatcher_role")),
    "payload_contract_version = " + str(d.get("payload_contract_version")),
    "required_field_count = " + str(len(d.get("required_payload_fields", []))),
    "optional_field_count = " + str(len(d.get("optional_payload_fields", []))),
    "forbidden_field_count = " + str(len(d.get("forbidden_payload_fields", []))),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "payload_contract_ready = " + str(d.get("payload_contract_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
