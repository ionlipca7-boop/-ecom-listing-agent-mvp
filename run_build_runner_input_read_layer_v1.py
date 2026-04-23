import json
from pathlib import Path

def main():
    connection = json.loads(Path("generator_runner_connection.json").read_text(encoding="utf-8"))
    input_file = connection.get("handoff_contract", {}).get("input_file", "generator_output_extended.json")
    payload = json.loads(Path(input_file).read_text(encoding="utf-8"))
    output = payload.get("output", {})
    layer = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "RUNNER_INPUT_READ_LAYER",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "source_connection": "generator_runner_connection.json",
        "input_file": input_file,
        "title_ready": bool(output.get("title")),
        "description_ready": bool(output.get("description")),
        "price_ready": bool(output.get("price")),
        "html_ready": bool(output.get("html")),
        "category_ready": bool(output.get("category")),
        "images_ready": bool(output.get("images")),
        "live_operations_enabled": False,
        "next_step": "connect_runner_to_input_layer"
    }
    Path("runner_input_read_layer.json").write_text(json.dumps(layer, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("RUNNER_INPUT_READ_LAYER_READY")

if __name__ == "__main__":
    main()
