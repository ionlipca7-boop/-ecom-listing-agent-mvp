import json
from pathlib import Path

base = Path(".")
state_file = base / "project_state.json"
checkpoint_file = base / "storage" / "checkpoints" / "runner_transition_checkpoint_v1.json"
archive_dir = base / "storage" / "memory" / "archive"
archive_dir.mkdir(parents=True, exist_ok=True)
output_file = archive_dir / "project_full_transition_archive_v1.json"

state = json.loads(state_file.read_text(encoding="utf-8"))
checkpoint = json.loads(checkpoint_file.read_text(encoding="utf-8"))

archive = {
    "status": "OK",
    "archive_type": "FULL_PROJECT_TRANSITION_V1",
    "project": state.get("project"),
    "mode": state.get("layer"),
    "phase": state.get("phase"),
    "current_phase": state.get("current_phase"),
    "current_step": state.get("current_step"),
    "active_stage": state.get("active_stage"),
    "last_successful_action": state.get("last_successful_action"),
    "next_allowed_action": state.get("next_allowed_action"),

    "runner_state": state.get("runner_state"),
    "runner_integrated": state.get("runner_integrated"),
    "runner_safe_blocked": state.get("runner_safe_blocked"),

    "checkpoint_summary": {
        "runner_pipeline_complete": checkpoint.get("runner_pipeline_complete"),
        "execution_allowed": checkpoint.get("execution_allowed"),
        "final_decision": checkpoint.get("final_decision"),
        "runner_live_permission": checkpoint.get("runner_live_permission"),
        "transition_state": checkpoint.get("transition_state")
    },

    "system_flags": {
        "live_operations_allowed": state.get("live_operations_allowed"),
        "migration_allowed": state.get("migration_allowed"),
        "side_branches_allowed": state.get("side_branches_allowed"),
        "n8n_ready": state.get("n8n_ready"),
        "compact_core_ready": state.get("compact_core_ready")
    },

    "next_step": "decide_next_project_specific_branch_after_runner_checkpoint",
    "archive_purpose": "safe_transition_to_new_chat_with_full_project_state"
}

output_file.write_text(json.dumps(archive, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "archive_created": output_file.exists(),
    "runner_pipeline_complete": checkpoint.get("runner_pipeline_complete"),
    "execution_allowed": checkpoint.get("execution_allowed"),
    "final_decision": checkpoint.get("final_decision"),
    "runner_live_permission": checkpoint.get("runner_live_permission"),
    "next_step": "ready_for_new_chat_transition"
}

print("FULL_PROJECT_TRANSITION_ARCHIVE_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
