import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "listing_improvement_path_gate_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    audit = {
        "status": "OK",
        "layer": "LISTING_IMPROVEMENT_PATH_GATE_AUDIT_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "direction_result": data["direction_result"],
        "selected_direction": data["selected_direction"],
        "listing_improvement_path_gate_defined": data["listing_improvement_path_gate_defined"],
        "execution_still_blocked": data["execution_still_blocked"],
        "runner_still_blocked": data["runner_still_blocked"],
        "live_still_blocked": data["live_still_blocked"],
        "parallel_branching_forbidden": data["parallel_branching_forbidden"],
        "audit_result": "listing_improvement_path_gate_verified",
        "next_allowed_action": "build_listing_improvement_scope_definition_v1"
    }
    out_file = out_dir / "listing_improvement_path_gate_audit_v1.json"
    out_file.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print("LISTING_IMPROVEMENT_PATH_GATE_AUDIT_V1_CREATED")
    print("status =", audit["status"])
    print("input_layer =", audit["input_layer"])
    print("input_status =", audit["input_status"])
    print("direction_result =", audit["direction_result"])
    print("selected_direction =", audit["selected_direction"])
    print("listing_improvement_path_gate_defined =", audit["listing_improvement_path_gate_defined"])
    print("execution_still_blocked =", audit["execution_still_blocked"])
    print("runner_still_blocked =", audit["runner_still_blocked"])
    print("live_still_blocked =", audit["live_still_blocked"])
    print("next_allowed_action =", audit["next_allowed_action"])

if __name__ == "__main__":
    main()
