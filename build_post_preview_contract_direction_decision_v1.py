import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "post_preview_contract_direction_plan_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    decision = {
        "status": "OK",
        "layer": "POST_PREVIEW_CONTRACT_DIRECTION_DECISION_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "preview_contract_chain_completed": data["preview_contract_chain_completed"],
        "direction_plan_defined": data["direction_plan_defined"],
        "direction_decision_defined": True,
        "decision_scope": "post_preview_contract_path_only",
        "selected_direction": "prepare_listing_improvement_path_gate_v1",
        "execution_still_blocked": True,
        "runner_still_blocked": True,
        "live_still_blocked": True,
        "parallel_branching_forbidden": True,
        "decision_result": "post_preview_contract_direction_locked",
        "next_allowed_action": "build_listing_improvement_path_gate_v1"
    }
    out_file = out_dir / "post_preview_contract_direction_decision_v1.json"
    out_file.write_text(json.dumps(decision, indent=2), encoding="utf-8")
    print("POST_PREVIEW_CONTRACT_DIRECTION_DECISION_V1_CREATED")
    print("status =", decision["status"])
    print("input_layer =", decision["input_layer"])
    print("input_status =", decision["input_status"])
    print("direction_decision_defined =", decision["direction_decision_defined"])
    print("selected_direction =", decision["selected_direction"])
    print("execution_still_blocked =", decision["execution_still_blocked"])
    print("runner_still_blocked =", decision["runner_still_blocked"])
    print("live_still_blocked =", decision["live_still_blocked"])
    print("next_allowed_action =", decision["next_allowed_action"])

if __name__ == "__main__":
    main()
