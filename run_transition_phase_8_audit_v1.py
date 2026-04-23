import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\memory\archive\transition_phase_8_to_next_chat_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\transition_phase_8_to_next_chat_v1_audit.txt")
lines = [
    "TRANSITION_PHASE_8_TO_NEXT_CHAT_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "phase_status = " + str(d.get("phase_status")),
    "direction_locked = " + str(d.get("direction_locked")),
    "selected_direction = " + str(d.get("selected_direction")),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "next_step = " + str(d.get("next_step"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
