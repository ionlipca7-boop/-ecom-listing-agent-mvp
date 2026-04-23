import json, pathlib
src = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\memory\archive\project_full_transition_archive_v1.json")
data = json.loads(src.read_text(encoding="utf-8"))
out = pathlib.Path(r"D:\ECOM_LISTING_AGENT_MVP\storage\audit\current_phase_audit_v1.txt")
lines = [
    "CURRENT_PHASE_AUDIT_V1",
    "status = " + str(data.get("status")),
    "project = " + str(data.get("project")),
    "mode = " + str(data.get("mode")),
    "phase = " + str(data.get("phase")),
    "current_phase = " + str(data.get("current_phase")),
    "current_step = " + str(data.get("current_step")),
    "active_stage = " + str(data.get("active_stage")),
    "last_successful_action = " + str(data.get("last_successful_action")),
    "next_allowed_action = " + str(data.get("next_allowed_action")),
    "runner_pipeline_complete = " + str(data.get("runner_state", {}).get("runner_pipeline_complete")),
    "execution_allowed = " + str(data.get("runner_state", {}).get("execution_allowed")),
    "final_decision = " + str(data.get("runner_state", {}).get("final_decision")),
    "runner_live_permission = " + str(data.get("runner_state", {}).get("runner_live_permission")),
    "runner_integrated = " + str(data.get("runner_integrated")),
    "runner_safe_blocked = " + str(data.get("runner_safe_blocked")),
    "live_operations_allowed = " + str(data.get("system_flags", {}).get("live_operations_allowed")),
    "migration_allowed = " + str(data.get("system_flags", {}).get("migration_allowed")),
    "side_branches_allowed = " + str(data.get("system_flags", {}).get("side_branches_allowed")),
    "n8n_ready = " + str(data.get("system_flags", {}).get("n8n_ready")),
    "compact_core_ready = " + str(data.get("system_flags", {}).get("compact_core_ready")),
    "canonical_position = PHASE_8_RUNNER_CHECKPOINT_INTEGRATED",
    "do_not_restart_from_manifest = True",
    "do_not_offer_live = True",
    "true_next_step = decide_next_project_specific_branch_after_runner_checkpoint"
]
out.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
