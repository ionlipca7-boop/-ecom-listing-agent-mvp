import json
from pathlib import Path

def main():
    ext_path = Path("generator_output_extended.json")
    val_path = Path("generator_extension_output_validation.json")

    result = {
        "status": "OK",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "EXTENSION_VALIDATION_GATE",
        "mode": "PROJECT_SPECIFIC_ONLY",
        "generator_output_extended_exists": ext_path.exists(),
        "generator_extension_output_validation_exists": val_path.exists()
    }

    if ext_path.exists():
        d = json.loads(ext_path.read_text(encoding="utf-8"))
        o = d.get("output", {})
        checks = {
            "status_is_extension_ready": d.get("status") == "GENERATOR_EXTENSION_OUTPUT_READY",
            "mode_is_project_specific": d.get("mode") == "PROJECT_SPECIFIC_ONLY",
            "title_exists": bool(o.get("title")),
            "description_exists": bool(o.get("description")),
            "price_positive": isinstance(o.get("price"), (int, float)) and o.get("price") 
            "draft_status_ok": o.get("status") == "draft",
            "html_exists": bool(o.get("html")),
            "category_exists": bool(o.get("category")),
        }
        validation = {
            "status": "OK" if all(checks.values()) else "FAIL",
            "project": "ECOM_LISTING_AGENT_MVP",
            "layer": "GENERATOR_EXTENSION_OUTPUT_VALIDATION",
            "mode": d.get("mode", "PROJECT_SPECIFIC_ONLY"),
            "checks": checks,
            "next_step": "archive_generator_extension_validation_result" if all(checks.values()) else "fix_generator_extension_output"
        }
        val_path.write_text(json.dumps(validation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["validation_written"] = True
    else:
        result["validation_written"] = False
        result["next_step"] = "restore_generator_output_extended"

    Path("extension_validation_gate_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("EXTENSION_VALIDATION_GATE_DONE")

if __name__ == "__main__":
    main()
