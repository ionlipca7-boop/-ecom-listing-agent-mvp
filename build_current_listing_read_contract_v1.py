import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "current_listing_read_plan_audit_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    contract = {
        "status": "OK",
        "layer": "CURRENT_LISTING_READ_CONTRACT_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "contract_defined": True,
        "scope_target": data["scope_target"],
        "read_mode": data["read_mode"],
        "inventory_read_required": True,
        "offer_read_required": True,
        "compare_input_required": True,
        "execution_still_blocked": True,
        "runner_still_blocked": True,
        "live_still_blocked": True,
        "parallel_branching_forbidden": True,
        "next_allowed_action": "build_current_listing_read_contract_audit_v1"
    }
    out_file = out_dir / "current_listing_read_contract_v1.json"
    out_file.write_text(json.dumps(contract, indent=2), encoding="utf-8")
    print("CURRENT_LISTING_READ_CONTRACT_V1_CREATED")
    print("status =", contract["status"])
    print("input_layer =", contract["input_layer"])
    print("input_status =", contract["input_status"])
    print("contract_defined =", contract["contract_defined"])
    print("scope_target =", contract["scope_target"])
    print("read_mode =", contract["read_mode"])
    print("inventory_read_required =", contract["inventory_read_required"])
    print("offer_read_required =", contract["offer_read_required"])
    print("compare_input_required =", contract["compare_input_required"])
    print("next_allowed_action =", contract["next_allowed_action"])

if __name__ == "__main__":
    main()
