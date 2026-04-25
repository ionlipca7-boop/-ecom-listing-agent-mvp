from pathlib import Path
import json
out_path = Path(r"storage\state_control\preview_contract_gap_decision_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "PREVIEW_CONTRACT_GAP_DECISION_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_phase": "PREVIEW_CONTRACT_FIRST_TECHNICAL_AUDIT_CONFIRMED",
    "input_layer": "PREVIEW_CONTRACT_INTEGRITY_AUDIT_V1",
    "decision_defined": True,
    "decision_scope": "preview_contract_only",
    "audit_result_confirmed": "preview_contract_path_integrity_confirmed",
    "gap_detected": False,
    "decision_summary": "no contract gap detected on preview contract path, safe to move to next preview contract control step",
    "still_blocked": {
        "runner_execution_now": True,
        "live_execution_now": True,
        "parallel_branching": True
    },
    "next_allowed_direction": "build_preview_contract_transition_gate_v1",
    "do_now": "build_preview_contract_transition_gate_v1",
    "one_next_step": "build_preview_contract_transition_gate_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("PREVIEW_CONTRACT_GAP_DECISION_V1_CREATED")
print("status =", data["status"])
print("gap_detected =", data["gap_detected"])
print("one_next_step =", data["one_next_step"])
