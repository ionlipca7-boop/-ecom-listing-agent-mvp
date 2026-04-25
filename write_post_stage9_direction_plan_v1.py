from pathlib import Path
import json
out_path = Path(r"storage\state_control\post_stage9_direction_plan_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "POST_STAGE9_DIRECTION_PLAN_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_stage": 9,
    "last_confirmed_completed_stage": 9,
    "current_phase": "POST_STAGE9_MANAGEMENT_CHECKPOINT",
    "direction_plan_defined": True,
    "current_state": {
        "compact_core_confirmed": True,
        "post_stage9_control_check_confirmed": True,
        "technical_build_allowed_now": False,
        "live_allowed_now": False,
        "parallel_branches_allowed": False
    },
    "allowed_paths": [
        "preview_execution_validation_planning",
        "runner_path_validation_planning",
        "project_specific_management_sequencing"
    ],
    "forbidden_paths": [
        "new_technical_layer_before_direction_plan_lock",
        "live_execution_jump",
        "n8n_jump",
        "parallel_branching",
        "return_to_pre_stage9_canonical_revalidation_as_next_step"
    ],
    "risk_zones": [
        "premature_technical_build",
        "execution_without_management_lock",
        "format_drift",
        "multi_step_drift"
    ],
    "selected_direction": "PREVIEW_EXECUTION_VALIDATION_PLANNING_V1",
    "selection_reason": "validate correct post_stage9 management direction before any technical expansion",
    "next_phase": "PREVIEW_EXECUTION_VALIDATION_PLANNING_V1",
    "do_now": "build_preview_execution_validation_planning_v1",
    "one_next_step": "build_preview_execution_validation_planning_v1",
    "execution_rules": [
        "project_specific_only",
        "one_step_only",
        "audit_first",
        "no_live",
        "no_parallel_branches",
        "no_new_technical_layer_before_management_confirmation"
    ]
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("POST_STAGE9_DIRECTION_PLAN_V1_CREATED")
print("status =", data["status"])
print("selected_direction =", data["selected_direction"])
print("one_next_step =", data["one_next_step"])
