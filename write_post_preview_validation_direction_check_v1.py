from pathlib import Path
import json
out_path = Path(r"storage\state_control\post_preview_validation_direction_check_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "POST_PREVIEW_VALIDATION_DIRECTION_CHECK_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_phase": "POST_STAGE9_PREVIEW_VALIDATION_MANAGEMENT",
    "input_layer": "PREVIEW_EXECUTION_VALIDATION_CHECKPOINT_V1",
    "direction_check_defined": True,
    "checkpoint_result_confirmed": True,
    "current_chain_status": "management_chain_complete",
    "still_blocked": {
        "technical_build_now": True,
        "runner_execution_now": True,
        "live_execution_now": True,
        "parallel_branching": True
    },
    "allowed_now": [
        "direction_selection_only",
        "single_next_phase_definition",
        "project_specific_management_continuation"
    ],
    "selected_direction": "BUILD_POST_PREVIEW_NEXT_PHASE_PLAN_V1",
    "selection_reason": "management_chain_is_complete_and_now_requires_single_next_phase_definition_before_any_execution_side_move",
    "do_now": "build_post_preview_next_phase_plan_v1",
    "one_next_step": "build_post_preview_next_phase_plan_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("POST_PREVIEW_VALIDATION_DIRECTION_CHECK_V1_CREATED")
print("status =", data["status"])
print("selected_direction =", data["selected_direction"])
print("one_next_step =", data["one_next_step"])
