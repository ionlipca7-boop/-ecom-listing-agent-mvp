from pathlib import Path
import json
out_path = Path(r"storage\state_control\preview_execution_validation_map_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "PREVIEW_EXECUTION_VALIDATION_MAP_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_stage": 9,
    "input_plan": "PREVIEW_EXECUTION_VALIDATION_PLANNING_V1",
    "map_defined": True,
    "validation_target": "compact_core_to_preview_management_path",
    "validation_sequence": [
        "confirm_compact_core_checkpoint_is_locked",
        "confirm_preview_contract_path_is_management_target",
        "confirm_no_technical_build_is_required_for_validation_map",
        "confirm_single_next_step_rule_is_preserved"
    ],
    "validation_inputs": [
        "compact_core_checkpoint_v1",
        "post_stage9_direction_plan_v1",
        "preview_execution_validation_planning_v1"
    ],
    "validation_constraints": {
        "project_specific_only": True,
        "technical_build_allowed": False,
        "runner_execution_allowed": False,
        "live_execution_allowed": False,
        "parallel_branches_allowed": False
    },
    "map_outputs": {
        "validation_checkpoints_defined": True,
        "validation_boundaries_defined": True,
        "single_followup_step_defined": True
    },
    "do_now": "build_preview_execution_validation_gate_v1",
    "one_next_step": "build_preview_execution_validation_gate_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("PREVIEW_EXECUTION_VALIDATION_MAP_V1_CREATED")
print("status =", data["status"])
print("one_next_step =", data["one_next_step"])
