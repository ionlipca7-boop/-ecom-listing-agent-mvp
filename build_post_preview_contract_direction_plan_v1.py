import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "preview_contract_completion_audit_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    plan = {
        "status": "OK",
        "layer": "POST_PREVIEW_CONTRACT_DIRECTION_PLAN_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "preview_contract_chain_completed": True,
        "preview_contract_completion_result": data["completion_result"],
        "direction_plan_defined": True,
        "allowed_scope": "post_preview_contract_planning_only",
        "execution_still_blocked": True,
        "runner_still_blocked": True,
        "live_still_blocked": True,
        "parallel_branching_forbidden": True,
        "next_allowed_action": "build_post_preview_contract_direction_decision_v1"
    }
    out_file = out_dir / "post_preview_contract_direction_plan_v1.json"
    out_file.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print("POST_PREVIEW_CONTRACT_DIRECTION_PLAN_V1_CREATED")
    print("status =", plan["status"])
    print("input_layer =", plan["input_layer"])
    print("input_status =", plan["input_status"])
    print("preview_contract_chain_completed =", plan["preview_contract_chain_completed"])
    print("preview_contract_completion_result =", plan["preview_contract_completion_result"])
    print("direction_plan_defined =", plan["direction_plan_defined"])
    print("execution_still_blocked =", plan["execution_still_blocked"])
    print("runner_still_blocked =", plan["runner_still_blocked"])
    print("live_still_blocked =", plan["live_still_blocked"])
    print("next_allowed_action =", plan["next_allowed_action"])

if __name__ == "__main__":
    main()
