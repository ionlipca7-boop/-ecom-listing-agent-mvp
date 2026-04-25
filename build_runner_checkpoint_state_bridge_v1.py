import json
from pathlib import Path

base = Path(".")
checkpoint_file = base / "storage" / "checkpoints" / "runner_transition_checkpoint_v1.json"
state_file = base / "project_state.json"
output_dir = base / "storage" / "state_bridge"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "runner_checkpoint_state_bridge_v1.json"

checkpoint_data = json.loads(checkpoint_file.read_text(encoding="utf-8"))
state_data = json.loads(state_file.read_text(encoding="utf-8"))

runner_state = {
    "status": "completed_blocked_safe",
    "checkpoint_layer": checkpoint_data.get("layer"),
    "runner_pipeline_complete": checkpoint_data.get("runner_pipeline_complete"),
    "execution_allowed": checkpoint_data.get("execution_allowed"),
    "final_decision": checkpoint_data.get("final_decision"),
    "runner_live_permission": checkpoint_data.get("runner_live_permission"),
    "transition_state": checkpoint_data.get("transition_state")
}

state_data["runner_state"] = runner_state
state_data["current_phase"] = "RUNNER_CHECKPOINT_INTEGRATED_V1"
state_data["last_successful_action"] = "build_runner_checkpoint_state_bridge_v1"
state_data["next_allowed_action"] = "decide_next_project_specific_branch_after_runner_checkpoint"

bridge = {
    "status": "OK",
    "layer": "RUNNER_CHECKPOINT_STATE_BRIDGE_V1",
    "mode": checkpoint_data.get("mode"),
    "checkpoint_file": str(checkpoint_file),
    "state_file": str(state_file),
    "runner_state_written": True,
    "current_phase": state_data.get("current_phase"),
    "last_successful_action": state_data.get("last_successful_action"),
    "next_allowed_action": state_data.get("next_allowed_action"),
    "runner_state": runner_state
}

state_file.write_text(json.dumps(state_data, indent=2, ensure_ascii=False), encoding="utf-8")
output_file.write_text(json.dumps(bridge, indent=2, ensure_ascii=False), encoding="utf-8")

audit = {
    "status": "OK",
    "layer": "RUNNER_CHECKPOINT_STATE_BRIDGE_V1",
    "mode": checkpoint_data.get("mode"),
    "runner_state_written": True,
    "runner_pipeline_complete": runner_state.get("runner_pipeline_complete"),
    "execution_allowed": runner_state.get("execution_allowed"),
    "final_decision": runner_state.get("final_decision"),
    "runner_live_permission": runner_state.get("runner_live_permission"),
    "current_phase": state_data.get("current_phase"),
    "next_allowed_action": state_data.get("next_allowed_action")
}

print("RUNNER_CHECKPOINT_STATE_BRIDGE_V1_AUDIT")
print(json.dumps(audit, indent=2, ensure_ascii=False))
