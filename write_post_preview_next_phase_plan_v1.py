from pathlib import Path
import json
out_path = Path(r"storage\state_control\post_preview_next_phase_plan_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "POST_PREVIEW_NEXT_PHASE_PLAN_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_phase": "POST_STAGE9_PREVIEW_VALIDATION_MANAGEMENT",
    "input_layer": "POST_PREVIEW_VALIDATION_DIRECTION_CHECK_V1",
    "plan_defined": True,
    "plan_scope": "management_only",
    "current_position": "post_preview_management_chain_complete",
    "still_blocked": {
        "technical_build_now": True,
        "runner_execution_now": True,
        "live_execution_now": True,
        "parallel_branching": True
    },
    "allowed_now": [
        "single_next_phase_lock",
        "management_transition_definition",
        "project_specific_continuation_only"
    ],
    "selected_next_phase": "PREVIEW_EXECUTION_READINESS_CHECK_V1",
    "selection_reason": "after management chain completion the next correct move is readiness check, not technical execution",
    "do_now": "build_preview_execution_readiness_check_v1",
    "one_next_step": "build_preview_execution_readiness_check_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("POST_PREVIEW_NEXT_PHASE_PLAN_V1_CREATED")
print("status =", data["status"])
print("selected_next_phase =", data["selected_next_phase"])
print("one_next_step =", data["one_next_step"])
