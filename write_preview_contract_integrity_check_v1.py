from pathlib import Path
import json
out_path = Path(r"storage\state_control\preview_contract_integrity_check_v1.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
data = {
    "status": "OK",
    "layer": "PREVIEW_CONTRACT_INTEGRITY_CHECK_V1",
    "project": "ECOM_LISTING_AGENT_MVP",
    "current_phase": "FIRST_SAFE_TECHNICAL_ENTRY_DEFINED",
    "input_layer": "FIRST_TECHNICAL_ENTRYPOINT_PLAN_V1",
    "check_defined": True,
    "check_scope": "preview_contract_only",
    "selected_entrypoint_confirmed": True,
    "integrity_targets": [
        "compact_core_preview_contract_v1",
        "compact_core_preview_verification_v1",
        "compact_core_preview_ready_gate_v1" 
    ],
    "check_rules": {
        "contract_surface_only": True,
        "no_runner_execution": True,
        "no_live_execution": True,
        "no_parallel_branching": True
    },
    "expected_result": "preview_contract_path_integrity_confirmed_or_gap_detected",
    "do_now": "build_preview_contract_integrity_audit_v1",
    "one_next_step": "build_preview_contract_integrity_audit_v1"
}
out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("PREVIEW_CONTRACT_INTEGRITY_CHECK_V1_CREATED")
print("status =", data["status"])
print("expected_result =", data["expected_result"])
print("one_next_step =", data["one_next_step"])
