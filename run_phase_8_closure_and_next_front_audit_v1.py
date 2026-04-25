import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\memory\archive\phase_8_closure_and_next_front_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
audit = d.get("canonical_audit_result", {})
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\phase_8_closure_and_next_front_v1_audit.txt")
lines = [
    "PHASE_8_CLOSURE_AND_NEXT_FRONT_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "phase_status = " + str(d.get("phase_status")),
    "phase_8_canon_complete = " + str(audit.get("phase_8_canon_complete")),
    "execution_allowed = " + str(audit.get("execution_allowed")),
    "final_decision = " + str(audit.get("final_decision")),
    "n8n_ready = " + str(audit.get("n8n_ready")),
    "chosen_next_front = " + str(d.get("chosen_next_front")),
    "chosen_next_step = " + str(d.get("chosen_next_step")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
