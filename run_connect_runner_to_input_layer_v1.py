import json
from pathlib import Path

def main():
    layer_data = json.loads(Path("runner_input_read_layer.json").read_text(encoding="utf-8"))
    payload = json.loads(Path(layer_data.get("input_file", "generator_output_extended.json")).read_text(encoding="utf-8"))
    output = payload.get("output", {})
    result = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "RUNNER_INPUT_CONNECTION",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "source_layer": "runner_input_read_layer.json",
        "runner_source": "runner_agent.py",
        "input_file": layer_data.get("input_file"),
        "input_ready": bool(output.get("title")) and bool(output.get("description")) and bool(output.get("price")) and bool(output.get("html")) and bool(output.get("category")) and bool(output.get("images")),
        "live_operations_enabled": False,
        "next_step": "build_runner_preview_layer"
    }
    Path("runner_input_connection.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("RUNNER_INPUT_CONNECTION_READY")

if __name__ == "__main__":
    main()
