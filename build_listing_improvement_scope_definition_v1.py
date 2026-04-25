import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "listing_improvement_path_gate_audit_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    scope = {
        "status": "OK",
        "layer": "LISTING_IMPROVEMENT_SCOPE_DEFINITION_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "listing_improvement_path_verified": True,
        "scope_defined": True,
        "scope_mode": "planning_only",
        "scope_target": "existing_working_listing_improvement",
        "allowed_actions": [
            "read_current_listing_state",
            "compare_current_vs_target",
            "define_revise_payload_scope"
        ],
        "execution_still_blocked": True,
        "runner_still_blocked": True,
        "live_still_blocked": True,
        "parallel_branching_forbidden": True,
        "next_allowed_action": "build_listing_improvement_scope_audit_v1"
    }
    out_file = out_dir / "listing_improvement_scope_definition_v1.json"
    out_file.write_text(json.dumps(scope, indent=2), encoding="utf-8")
    print("LISTING_IMPROVEMENT_SCOPE_DEFINITION_V1_CREATED")
    print("status =", scope["status"])
    print("input_layer =", scope["input_layer"])
    print("input_status =", scope["input_status"])
    print("listing_improvement_path_verified =", scope["listing_improvement_path_verified"])
    print("scope_defined =", scope["scope_defined"])
    print("scope_mode =", scope["scope_mode"])
    print("scope_target =", scope["scope_target"])
    print("execution_still_blocked =", scope["execution_still_blocked"])
    print("runner_still_blocked =", scope["runner_still_blocked"])
    print("live_still_blocked =", scope["live_still_blocked"])
    print("next_allowed_action =", scope["next_allowed_action"])

if __name__ == "__main__":
    main()
