import json
from pathlib import Path

def main():
    src = Path("generator_output_extended.json")
    if not src.exists():
        result = {
            "status": "FAIL",
            "project": "ECOM_LISTING_AGENT_MVP",
            "layer": "GENERATOR_EXTENSION_OUTPUT_VALIDATION",
            "mode": "PROJECT_SPECIFIC_ONLY",
            "checks": {"source_exists": False},
            "next_step": "restore_generator_output_extended"
        }
        Path("generator_extension_output_validation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("GENERATOR_EXTENSION_OUTPUT_VALIDATED")
        return

    d = json.loads(src.read_text(encoding="utf-8"))
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
    result = {
        "status": "OK" if all(checks.values()) else "FAIL",
        "project": "ECOM_LISTING_AGENT_MVP",
        "layer": "GENERATOR_EXTENSION_OUTPUT_VALIDATION",
        "mode": d.get("mode", "PROJECT_SPECIFIC_ONLY"),
        "checks": checks,
        "next_step": "archive_generator_extension_validation_result" if all(checks.values()) else "fix_generator_extension_output"
    }
    Path("generator_extension_output_validation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_EXTENSION_OUTPUT_VALIDATED")

if __name__ == "__main__":
    main()
