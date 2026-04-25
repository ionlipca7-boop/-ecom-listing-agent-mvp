import json
from pathlib import Path

def main():
    control = json.loads(Path("control_layer_review.json").read_text(encoding="utf-8"))
    contract = json.loads(Path("generator_input_contract.json").read_text(encoding="utf-8"))
    sample = json.loads(Path("generator_input_sample.json").read_text(encoding="utf-8"))
    output = json.loads(Path("generator_output.json").read_text(encoding="utf-8"))
    validation = json.loads(Path("generator_output_validation.json").read_text(encoding="utf-8"))
    snapshot = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "GENERATOR_STATUS_SNAPSHOT",
        "mode": control.get("mode"),
        "control_status": control.get("status"),
        "canonical_line_complete": control.get("canonical_line_complete"),
        "history_valid": control.get("history_valid"),
        "input_contract_ready": contract.get("status") == "OK",
        "input_sample_ready": sample.get("status") == "OK",
        "output_ready": output.get("status") == "GENERATOR_OUTPUT_READY",
        "validation_ready": validation.get("status") == "OK",
        "live_operations_enabled": False,
        "next_step": "prepare_next_project_specific_generator_extension"
    }
    Path("generator_status_snapshot.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_STATUS_SNAPSHOT_CREATED")

if __name__ == "__main__":
    main()
