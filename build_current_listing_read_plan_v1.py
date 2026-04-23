import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "listing_improvement_scope_audit_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    plan = {
        "status": "OK",
        "layer": "CURRENT_LISTING_READ_PLAN_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "scope_target": data["scope_target"],
        "read_plan_defined": True,
        "read_mode": "current_listing_state_only",
        "read_sequence": [
            "read_inventory_first",
            "read_offer_second",
            "prepare_compare_input"
        ],
        "execution_still_blocked": True,
        "runner_still_blocked": True,
        "live_still_blocked": True,
        "parallel_branching_forbidden": True,
        "next_allowed_action": "build_current_listing_read_plan_audit_v1"
    }
    out_file = out_dir / "current_listing_read_plan_v1.json"
    out_file.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print("CURRENT_LISTING_READ_PLAN_V1_CREATED")
    print("status =", plan["status"])
    print("input_layer =", plan["input_layer"])
    print("input_status =", plan["input_status"])
    print("scope_target =", plan["scope_target"])
    print("read_plan_defined =", plan["read_plan_defined"])
    print("read_mode =", plan["read_mode"])
    print("execution_still_blocked =", plan["execution_still_blocked"])
    print("runner_still_blocked =", plan["runner_still_blocked"])
    print("live_still_blocked =", plan["live_still_blocked"])
    print("next_allowed_action =", plan["next_allowed_action"])

if __name__ == "__main__":
    main()
