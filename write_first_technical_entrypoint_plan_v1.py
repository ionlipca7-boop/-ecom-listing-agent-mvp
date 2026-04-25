from pathlib import Path
import json
out_path = Path(r"storage\state_control\first_technical_entrypoint_plan_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "FIRST_TECHNICAL_ENTRYPOINT_PLAN_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_phase": "POST_STAGE9_MANAGEMENT_FINALIZED",
    "input_layer": "PREVIEW_EXECUTION_READINESS_DECISION_V1",
    "plan_defined": True,
    "plan_scope": "first_safe_technical_entry_definition_only",
    "management_completion_confirmed": True,
    "candidate_entrypoints": [
        "preview_contract_integrity_check",
        "runner_payload_contract_check",
        "delivery_state_contract_check"
    ],
    "selection_rule": "choose_the_lowest_risk_contract_validation_entrypoint_before_any_execution_logic",
    "selected_entrypoint": "preview_contract_integrity_check",
    "selection_reason": "preview_contract_path_is_the_nearest_safe_technical_surface_after_management_completion",
    "still_blocked": {
        "runner_execution_now": True,
        "live_execution_now": True,
        "parallel_branching": True
    },
    "do_now": "build_preview_contract_integrity_check_v1",
    "one_next_step": "build_preview_contract_integrity_check_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("FIRST_TECHNICAL_ENTRYPOINT_PLAN_V1_CREATED")
print("status =", data["status"])
print("selected_entrypoint =", data["selected_entrypoint"])
print("one_next_step =", data["one_next_step"])
