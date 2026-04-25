import json
from pathlib import Path

def main():
    d = json.loads(Path("generator_output.json").read_text(encoding="utf-8"))
    output = d.get("output", {})
    title = output.get("title", "")
    description = output.get("description", "")
    price = output.get("price", 0)
    draft_status = output.get("status")
    checks = {
        "status_is_ready": d.get("status") == "GENERATOR_OUTPUT_READY",
        "mode_is_project_specific": d.get("mode") == "PROJECT_SPECIFIC_ONLY",
        "title_exists": bool(title),
        "title_len_le_80": len(title) <= 80,
        "description_exists": bool(description),
        "price_positive": isinstance(price, (int, float)) and price > 0,
        "draft_status_ok": draft_status == "draft"
    }
    result = {
        "status": "OK" if all(checks.values()) else "FAIL",
        "layer": "GENERATOR_OUTPUT_VALIDATION",
        "mode": d.get("mode"),
        "checks": checks,
        "next_step": "archive_generator_validation_result" if all(checks.values()) else "fix_generator_output"
    }
    Path("generator_output_validation.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("GENERATOR_OUTPUT_VALIDATED")

if __name__ == "__main__":
    main()
