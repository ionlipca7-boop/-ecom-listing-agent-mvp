import json
from pathlib import Path

def main():
    root = Path("D:\\ECOM_LISTING_AGENT_MVP")
    in_file = root / "storage" / "state_control" / "preview_contract_post_gate_direction_decision_v1.json"
    out_dir = root / "storage" / "state_control"
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(in_file.read_text(encoding="utf-8"))
    summary = {
        "status": "OK",
        "layer": "PREVIEW_CONTRACT_TECHNICAL_ENTRY_SUMMARY_V1",
        "project": "ECOM_LISTING_AGENT_MVP",
        "input_layer": data["layer"],
        "input_status": data["status"],
        "technical_entry_surface": "preview_contract",
        "technical_entry_path_confirmed": data["technical_entry_path_confirmed"],
        "direction_result": data["decision_result"],
        "execution_still_blocked": data["execution_still_blocked"],
        "runner_still_blocked": data["runner_still_blocked"],
        "live_still_blocked": data["live_still_blocked"],
        "parallel_branching_forbidden": data["parallel_branching_forbidden"],
        "summary_result": "preview_contract_technical_entry_chain_confirmed",
        "next_allowed_action": "build_preview_contract_completion_audit_v1"
    }
    out_file = out_dir / "preview_contract_technical_entry_summary_v1.json"
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("PREVIEW_CONTRACT_TECHNICAL_ENTRY_SUMMARY_V1_CREATED")
    print("status =", summary["status"])
    print("input_layer =", summary["input_layer"])
    print("input_status =", summary["input_status"])
    print("technical_entry_surface =", summary["technical_entry_surface"])
    print("technical_entry_path_confirmed =", summary["technical_entry_path_confirmed"])
    print("direction_result =", summary["direction_result"])
    print("execution_still_blocked =", summary["execution_still_blocked"])
    print("runner_still_blocked =", summary["runner_still_blocked"])
    print("live_still_blocked =", summary["live_still_blocked"])
    print("next_allowed_action =", summary["next_allowed_action"])

if __name__ == "__main__":
    main()
