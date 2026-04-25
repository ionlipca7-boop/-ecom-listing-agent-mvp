import json
from pathlib import Path

def main():
    base = json.loads(Path("generator_output.json").read_text(encoding="utf-8"))
    ext = json.loads(Path("generator_output_extended.json").read_text(encoding="utf-8"))
    val = json.loads(Path("generator_extension_output_validation.json").read_text(encoding="utf-8"))

    snapshot = {
        "status": "OK",
        "layer": "GENERATOR_FULL_STATUS_SNAPSHOT",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "base_output_ready": base.get("status") == "GENERATOR_OUTPUT_READY",
        "extension_output_ready": ext.get("status") == "GENERATOR_EXTENSION_OUTPUT_READY",
        "validation_ready": val.get("status") == "OK",
        "live_operations_enabled": False,
        "next_step": "prepare_generator_runner_connection"
    }

    Path("generator_full_status_snapshot.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_FULL_STATUS_SNAPSHOT_READY")

if __name__ == "__main__":
    main()
