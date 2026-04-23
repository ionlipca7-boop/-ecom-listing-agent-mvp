import json
from pathlib import Path

def main():
    output_data = json.loads(Path("generator_output.json").read_text(encoding="utf-8"))
    ext_data = json.loads(Path("generator_extension_sample.json").read_text(encoding="utf-8"))
    output = output_data.get("output", {})
    ext_input = ext_data.get("extension_input", {})
    title = output.get("title", "")
    description = output.get("description", "")
    html_template = ext_input.get("html_template", "")
    html = html_template.replace("{title}", title).replace("{description}", description)
    output["html"] = html
    output["category"] = ext_input.get("category_hint")
    output["images"] = ext_input.get("images_hint", [])
    output_data["status"] = "GENERATOR_EXTENSION_OUTPUT_READY"
    output_data["extension_source"] = "generator_extension_sample.json"
    output_data["next"] = "validate_generator_extension_output"
    Path("generator_output_extended.json").write_text(json.dumps(output_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_EXTENSION_CONNECTED")

if __name__ == "__main__":
    main()
