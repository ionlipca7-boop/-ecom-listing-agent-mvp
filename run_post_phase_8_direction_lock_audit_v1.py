import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\post_phase_8_direction_lock_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\post_phase_8_direction_lock_v1_audit.txt")
lines = [
    "POST_PHASE_8_DIRECTION_LOCK_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "phase_status = " + str(d.get("phase_status")),
    "direction_lock_version = " + str(d.get("direction_lock_version")),
    "single_direction_required = " + str(d.get("single_direction_required")),
    "parallel_direction_forbidden = " + str(d.get("parallel_direction_forbidden")),
    "selected_direction = " + str(d.get("selected_direction")),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "final_decision = " + str(d.get("final_decision")),
    "direction_lock_ready = " + str(d.get("direction_lock_ready")),
    "next_allowed_action = " + str(d.get("next_allowed_action"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
