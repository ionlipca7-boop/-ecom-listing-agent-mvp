import json
from pathlib import Path

def main():
    snapshot = json.loads(Path("generator_full_status_snapshot.json").read_text(encoding="utf-8"))
    data = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "GENERATOR_RUNNER_CONNECTION",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "source_snapshot": "generator_full_status_snapshot.json",
        "generator_ready": bool(snapshot.get("base_output_ready")) and bool(snapshot.get("extension_output_ready")) and bool(snapshot.get("validation_ready")),
        "runner_source": "runner_agent.py",
        "handoff_contract": {
            "input_file": "generator_output_extended.json",
            "receiver": "runner_agent.py",
            "mode": "PROJECT_SPECIFIC_ONLY",
            "live_operations_enabled": False
        },
        "next_step": "build_runner_input_read_layer"
    }
    Path("generator_runner_connection.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_RUNNER_CONNECTION_READY")

if __name__ == "__main__":
    main()
