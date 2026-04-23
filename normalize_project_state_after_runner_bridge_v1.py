import json
from pathlib import Path

base = Path(".")
state_file = base / "project_state.json"
output_dir = base / "storage" / "state_normalization"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "project_state_normalized_v1.json"

state_data = json.loads(state_file.read_text(encoding="utf-8"))
runner_state = state_data.get("runner_state") or {}

state_data["current_step"] = "runner_checkpoint_integrated"
state_data["next_step"] = "decide_next_project_specific_branch_after_runner_checkpoint"
state_data["active_stage"] = "runner_checkpoint_integrated"
state_data["current_focus"] = "normalize_control_state_before_n8n_stage"
state_data["n8n_ready"] = False
state_data["compact_core_ready"] = False
state_data["current_phase"] = "RUNNER_CHECKPOINT_INTEGRATED_V1"
state_data["last_successful_action"] = "normalize_project_state_after_runner_bridge_v1"
state_data["next_allowed_action"] = "decide_next_project_specific_branch_after_runner_checkpoint"
state_data["runner_integrated"] = True
state_data["runner_safe_blocked"] = runner_state.get("final_decision") == "KEEP_BLOCKED"

normalized = {
    "status": "OK",
    "layer": "NORMALIZE_PROJECT_STATE_AFTER_RUNNER_BRIDGE_V1",
    "project": state_data.get("project"),
    "state_file": str(state_file),
    "phase": state_data.get("phase"),
    "current_step": state_data.get("current_step"),
    "next_step": state_data.get("next_step"),
    "active_stage": state_data.get("active_stage"),
    "current_phase": state_data.get("current_phase"),
    "last_successful_action": state_data.get("last_successful_action"),
    "next_allowed_action": state_data.get("next_allowed_action"),
    "runner_integrated": state_data.get("runner_integrated"),
    "runner_safe_blocked": state_data.get("runner_safe_blocked"),
    "n8n_ready": state_data.get("n8n_ready"),
    "compact_core_ready": state_data.get("compact_core_ready")
}

state_file.write_text(json.dumps(state_data, indent=2, ensure_ascii=False), encoding="utf-8")
output_file.write_text(json.dumps(normalized, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "NORMALIZE_PROJECT_STATE_AFTER_RUNNER_BRIDGE_V1",
    "phase": state_data.get("phase"),
    "current_step": state_data.get("current_step"),
    "next_step": state_data.get("next_step"),
    "active_stage": state_data.get("active_stage"),
    "current_phase": state_data.get("current_phase"),
    "runner_integrated": state_data.get("runner_integrated"),
    "runner_safe_blocked": state_data.get("runner_safe_blocked"),
    "n8n_ready": state_data.get("n8n_ready"),
    "compact_core_ready": state_data.get("compact_core_ready"),
    "next_allowed_action": state_data.get("next_allowed_action")
}

print("NORMALIZE_PROJECT_STATE_AFTER_RUNNER_BRIDGE_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
