import json, pathlib
p = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\state_control\post_runner_branch_decision_v1.json")
d = json.loads(p.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\post_runner_branch_decision_v1_audit.txt")
lines = [
    "POST_RUNNER_BRANCH_DECISION_V1_AUDIT",
    "status = " + str(d.get("status")),
    "phase = " + str(d.get("phase")),
    "current_phase = " + str(d.get("current_phase")),
    "runner_pipeline_complete = " + str(d.get("runner_pipeline_complete")),
    "execution_allowed = " + str(d.get("execution_allowed")),
    "final_decision = " + str(d.get("final_decision")),
    "selected_branch = " + str(d.get("selected_branch")),
    "next_allowed_action = " + str(d.get("next_allowed_action")),
    "do_not_restart_from_manifest = " + str(d.get("do_not_restart_from_manifest")),
    "do_not_offer_live = " + str(d.get("do_not_offer_live"))
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
