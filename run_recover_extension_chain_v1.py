import json
from pathlib import Path

def main():
    result = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "RECOVER_EXTENSION_CHAIN",
        "mode": "PROJECT_SPECIFIC_ONLY"
    }

    base_path = Path("generator_output.json")
    ext_sample_path = Path("generator_extension_sample.json")
    ext_output_path = Path("generator_output_extended.json")
    validation_path = Path("generator_extension_output_validation.json")
    gate_path = Path("extension_validation_gate_result.json")

    result["generator_output_exists"] = base_path.exists()
    result["generator_extension_sample_exists"] = ext_sample_path.exists()
    result["generator_output_extended_exists_before"] = ext_output_path.exists()
    result["generator_extension_output_validation_exists_before"] = validation_path.exists()

    if not base_path.exists() or not ext_sample_path.exists():
        result["status"] = "FAIL"
        result["next_step"] = "restore_generator_base_or_extension_sample"
        gate_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("RECOVER_EXTENSION_CHAIN_DONE")
        return

    base_data = json.loads(base_path.read_text(encoding="utf-8"))
    ext_data = json.loads(ext_sample_path.read_text(encoding="utf-8"))
    output = base_data.get("output", {})
    ext_input = ext_data.get("extension_input", {})

    title = output.get("title", "")
    description = output.get("description", "")
    html_template = ext_input.get("html_template", "")
    html = html_template.replace("{title}", title).replace("{description}", description)

    output["html"] = html
    output["category"] = ext_input.get("category_hint")
    output["images"] = ext_input.get("images_hint", [])
    base_data["status"] = "GENERATOR_EXTENSION_OUTPUT_READY"
    base_data["extension_source"] = "generator_extension_sample.json"
    base_data["next"] = "archive_generator_extension_validation_result"
    ext_output_path.write_text(json.dumps(base_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    d = json.loads(ext_output_path.read_text(encoding="utf-8"))
    o = d.get("output", {})
    checks = {
        "source_exists": True,
        "status_is_extension_ready": d.get("status") == "GENERATOR_EXTENSION_OUTPUT_READY",
        "mode_is_project_specific": d.get("mode") == "PROJECT_SPECIFIC_ONLY",
        "title_exists": bool(o.get("title")),
        "description_exists": bool(o.get("description")),
        "price_positive": isinstance(o.get("price"), (int, float)) and o.get("price") > 0,
        "draft_status_ok": o.get("status") == "draft",
        "html_exists": bool(o.get("html")),
        "category_exists": bool(o.get("category")),
        "images_count_ge_1": len(o.get("images", [])) >= 
    }

    validation = {
        "status": "OK" if all(checks.values()) else "FAIL",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "GENERATOR_EXTENSION_OUTPUT_VALIDATION",
        "mode": d.get("mode", "PROJECT_SPECIFIC_ONLY"),
        "checks": checks,
        "next_step": "archive_generator_extension_validation_result" if all(checks.values()) else "fix_generator_extension_output"
    }
    validation_path.write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result["generator_output_extended_exists_after"] = ext_output_path.exists()
    result["generator_extension_output_validation_exists_after"] = validation_path.exists()
    result["validation_status"] = validation.get("status")
    result["next_step"] = validation.get("next_step")
    gate_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("RECOVER_EXTENSION_CHAIN_DONE")

if __name__ == "__main__":
    main()
