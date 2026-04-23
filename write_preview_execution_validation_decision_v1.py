from pathlib import Path
import json
out_path = Path(r"storage\state_control\preview_execution_validation_decision_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "PREVIEW_EXECUTION_VALIDATION_DECISION_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_phase": "POST_STAGE9_PREVIEW_VALIDATION_MANAGEMENT",
    "input_layer": "PREVIEW_EXECUTION_VALIDATION_GATE_V1",
    "decision_defined": True,
    "decision_scope": "management_only",
    "decision_summary": "preview validation path remains approved only as management sequence without technical execution",
    "decision_points": {
        "management_path_confirmed": True,
        "technical_build_still_blocked": True,
        "runner_execution_still_blocked": True,
        "live_execution_still_blocked": True,
        "single_next_step_preserved": True
    },
    "selected_decision": "PREPARE_PREVIEW_EXECUTION_VALIDATION_SUMMARY_V1",
    "rejected_directions": [
        "technical_layer_build_now",
        "runner_flow_execution_now",
        "live_flow_execution_now",
        "parallel_branch_opening"
    ],
    "do_now": "build_preview_execution_validation_summary_v1",
    "one_next_step": "build_preview_execution_validation_summary_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("PREVIEW_EXECUTION_VALIDATION_DECISION_V1_CREATED")
print("status =", data["status"])
print("selected_decision =", data["selected_decision"])
print("one_next_step =", data["one_next_step"])
