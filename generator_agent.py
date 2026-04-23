import json
from pathlib import Path

def run_generator():
    control_path = Path("control_layer_review.json")
    sample_path = Path("generator_input_sample.json")

    if not control_path.exists():
        return {"status": "ERROR", "reason": "control_layer_missing", "next": "restore_source_of_truth"}
    if not sample_path.exists():
        return {"status": "ERROR", "reason": "generator_input_sample_missing", "next": "prepare_generator_input_sample"}

    control = json.loads(control_path.read_text(encoding="utf-8"))
    sample = json.loads(sample_path.read_text(encoding="utf-8"))

    control_complete = bool(control.get("control_layer_complete")) or control.get("status") == "CONTROL_LAYER_COMPLETE"
    mode = control.get("mode", "PROJECT_SPECIFIC_ONLY")

    if not control_complete:
        return {"status": "BLOCKED", "reason": "control_layer_not_complete", "next": "inspect_control_layer_review"}

    data = sample.get("input", {})
    product_title = data.get("product_title", "")
    product_type = data.get("product_type", "")
    specs = data.get("product_specs", {})
    price_hint = data.get("price_hint", 0)

    title = product_title[:80]
    description = f"{product_type} | Leistung: {specs.get('power', '')} | Lange: {specs.get('length', '')} | Funktion: {specs.get('function', '')}"

    return {
        "status": "GENERATOR_OUTPUT_READY",
        "mode": mode,
        "source_of_truth": "control_layer_review.json",
        "input_source": "generator_input_sample.json",
        "output": {
            "title": title,
            "description": description,
            "price": price_hint,
            "status": "draft"
        },
        "next": "persist_generator_output"
    }

if __name__ == "__main__":
    result = run_generator()
    print(json.dumps(result, indent=2, ensure_ascii=False))
