import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "post_preview_contract_direction_decision_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    gate = {
        "status": "OK",
        "layer": "LISTING_IMPROVEMENT_PATH_GATE_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "direction_result": data["decision_result"],
        "selected_direction": data["selected_direction"],
        "listing_improvement_path_gate_defined": True,
        "allowed_scope": "listing_improvement_path_control_only",
        "execution_still_blocked": True,
        "runner_still_blocked": True,
        "live_still_blocked": True,
        "parallel_branching_forbidden": True,
        "next_allowed_action": "build_listing_improvement_path_gate_audit_v1"
    }
    out_file = out_dir / "listing_improvement_path_gate_v1.json"
    out_file.write_text(json.dumps(gate, indent=2), encoding="utf-8")
    print("LISTING_IMPROVEMENT_PATH_GATE_V1_CREATED")
    print("status =", gate["status"])
    print("input_layer =", gate["input_layer"])
    print("input_status =", gate["input_status"])
    print("direction_result =", gate["direction_result"])
    print("selected_direction =", gate["selected_direction"])
    print("listing_improvement_path_gate_defined =", gate["listing_improvement_path_gate_defined"])
    print("execution_still_blocked =", gate["execution_still_blocked"])
    print("runner_still_blocked =", gate["runner_still_blocked"])
    print("live_still_blocked =", gate["live_still_blocked"])
    print("next_allowed_action =", gate["next_allowed_action"])

if __name__ == "__main__":
    main()
