from pathlib import Path
import json
out_path = Path(r"storage\state_control\preview_execution_validation_planning_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "PREVIEW_EXECUTION_VALIDATION_PLANNING_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_stage": 9,
    "input_direction_plan": "POST_STAGE9_DIRECTION_PLAN_V1",
    "planning_defined": True,
    "purpose": "define management validation scope for preview execution path without building technical layer",
    "validation_scope": {
        "compact_core_to_preview_path_only": True,
        "technical_build_in_scope": False,
        "live_execution_in_scope": False,
        "runner_handoff_execution_in_scope": False
    },
    "must_validate": [
        "preview_path_is_next_correct_management_target",
        "compact_core_contract_remains_intact",
        "preview_validation_can_be_planned_without_technical_jump",
        "one_step_only_rule_remains_active"
    ],
    "must_not_do": [
        "build_new_technical_layer",
        "execute_runner_flow",
        "start_live_flow",
        "open_parallel_branch"
    ],
    "expected_output": {
        "management_validation_map": True,
        "preview_path_constraints": True,
        "single_next_step_after_planning": True
    },
    "do_now": "build_preview_execution_validation_map_v1",
    "one_next_step": "build_preview_execution_validation_map_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("PREVIEW_EXECUTION_VALIDATION_PLANNING_V1_CREATED")
print("status =", data["status"])
print("one_next_step =", data["one_next_step"])
