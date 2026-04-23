import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
MULTI_FILE = EXPORTS_DIR / "multi_listing_generator_v1.json"
GROWTH_FILE = EXPORTS_DIR / "control_room_growth_status_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "variant_selector_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def select_variant(variants):
    if not variants:
        return None
    for variant in variants:
        angle = str(variant.get("angle", ""))
        if angle == "baseline_ai_title":
            return variant
    return variants[0]

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    multi = read_json(MULTI_FILE)
    growth = read_json(GROWTH_FILE)

    growth_status = "MISSING"
    variants = []
    selected_variant = None
    selection_status = "WAITING"
    next_step = "CHECK_GROWTH_LAYER_FIRST"

    if growth:
        growth_status = growth.get("growth_status", "MISSING")

    if multi:
        variants = multi.get("variants", [])

    if growth_status == "READY" and variants:
        selected_variant = select_variant(variants)
        selection_status = "READY"
        next_step = "USE_SELECTED_VARIANT_FOR_NEXT_EXECUTION_LAYER"

    selected_variant_id = ""
    selected_title = ""
    selected_angle = ""
    variant_count = len(variants)

    if selected_variant:
        selected_variant_id = selected_variant.get("variant_id", "")
        selected_title = selected_variant.get("title", "")
        selected_price = selected_variant.get("price", 0)
        selected_angle = selected_variant.get("angle", "")

    output = {
        "selection_status": selection_status,
        "next_step": next_step,
        "summary": {
            "growth_status": growth_status,
            "variant_count": variant_count,
            "selected_variant_id": selected_variant_id,
            "selected_title": selected_title,
            "selected_price": selected_price,
            "selected_angle": selected_angle
        },
        "selected_variant": selected_variant,
        "variants": variants,
        "inputs": {
            "multi_file": str(MULTI_FILE),
            "growth_file": str(GROWTH_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("VARIANT_SELECTOR_V1:")
    print("selection_status:", output["selection_status"])
    print("growth_status:", output["summary"]["growth_status"])
    print("variant_count:", output["summary"]["variant_count"])
    print("selected_variant_id:", output["summary"]["selected_variant_id"])
    print("selected_angle:", output["summary"]["selected_angle"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
