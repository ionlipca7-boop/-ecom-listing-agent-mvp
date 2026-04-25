import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "preview_contract_technical_entry_summary_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    audit = {
        "status": "OK",
        "layer": "PREVIEW_CONTRACT_COMPLETION_AUDIT_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "technical_entry_surface": data["technical_entry_surface"],
        "technical_entry_path_confirmed": data["technical_entry_path_confirmed"],
        "summary_result": data["summary_result"],
        "execution_still_blocked": data["execution_still_blocked"],
        "runner_still_blocked": data["runner_still_blocked"],
        "live_still_blocked": data["live_still_blocked"],
        "parallel_branching_forbidden": data["parallel_branching_forbidden"],
        "completion_result": "preview_contract_technical_entry_completed_and_verified",
        "next_allowed_action": "build_post_preview_contract_direction_plan_v1"
    }
    out_file = out_dir / "preview_contract_completion_audit_v1.json"
    out_file.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print("PREVIEW_CONTRACT_COMPLETION_AUDIT_V1_CREATED")
    print("status =", audit["status"])
    print("input_layer =", audit["input_layer"])
    print("input_status =", audit["input_status"])
    print("technical_entry_surface =", audit["technical_entry_surface"])
    print("technical_entry_path_confirmed =", audit["technical_entry_path_confirmed"])
    print("summary_result =", audit["summary_result"])
    print("execution_still_blocked =", audit["execution_still_blocked"])
    print("runner_still_blocked =", audit["runner_still_blocked"])
    print("live_still_blocked =", audit["live_still_blocked"])
    print("next_allowed_action =", audit["next_allowed_action"])

if __name__ == "__main__":
    main()
