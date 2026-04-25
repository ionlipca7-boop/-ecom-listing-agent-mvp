import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "preview_contract_transition_gate_audit_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    decision = {
        "status": "OK",
        "layer": "PREVIEW_CONTRACT_POST_GATE_DIRECTION_DECISION_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "post_gate_decision_defined": True,
        "decision_scope": "preview_contract_path_only",
        "technical_entry_path_confirmed": True,
        "execution_still_blocked": True,
        "runner_still_blocked": True,
        "live_still_blocked": True,
        "parallel_branching_forbidden": True,
        "decision_result": "preview_contract_post_gate_direction_locked",
        "next_allowed_action": "build_preview_contract_technical_entry_summary_v1"
    }
    out_file = out_dir / "preview_contract_post_gate_direction_decision_v1.json"
    out_file.write_text(json.dumps(decision, indent=2), encoding="utf-8")
    print("PREVIEW_CONTRACT_POST_GATE_DIRECTION_DECISION_V1_CREATED")
    print("status =", decision["status"])
    print("input_layer =", decision["input_layer"])
    print("input_status =", decision["input_status"])
    print("post_gate_decision_defined =", decision["post_gate_decision_defined"])
    print("technical_entry_path_confirmed =", decision["technical_entry_path_confirmed"])
    print("execution_still_blocked =", decision["execution_still_blocked"])
    print("runner_still_blocked =", decision["runner_still_blocked"])
    print("live_still_blocked =", decision["live_still_blocked"])
    print("next_allowed_action =", decision["next_allowed_action"])

if __name__ == "__main__":
    main()
