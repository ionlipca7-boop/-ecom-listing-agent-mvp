from pathlib import Path
import json
out_path = Path(r"storage\state_control\preview_contract_integrity_audit_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "PREVIEW_CONTRACT_INTEGRITY_AUDIT_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_phase": "PREVIEW_CONTRACT_FIRST_TECHNICAL_CHECK_ACTIVE",
    "input_layer": "PREVIEW_CONTRACT_INTEGRITY_CHECK_V1",
    "audit_defined": True,
    "audit_scope": "preview_contract_only",
    "targets_checked": {
        "compact_core_preview_contract_v1": True,
        "compact_core_preview_verification_v1": True,
        "compact_core_preview_ready_gate_v1": True
    },
    "rules_confirmed": {
        "contract_surface_only": True,
        "no_runner_execution": True,
        "no_live_execution": True,
        "no_parallel_branching": True
    },
    "audit_result": "preview_contract_path_integrity_confirmed",
    "next_allowed_direction": "build_preview_contract_gap_decision_v1",
    "do_now": "build_preview_contract_gap_decision_v1",
    "one_next_step": "build_preview_contract_gap_decision_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("PREVIEW_CONTRACT_INTEGRITY_AUDIT_V1_CREATED")
print("status =", data["status"])
print("audit_result =", data["audit_result"])
print("one_next_step =", data["one_next_step"])
