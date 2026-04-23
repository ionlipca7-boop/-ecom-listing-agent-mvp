import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
PERFORMANCE_FILE = EXPORTS_DIR / "listing_performance_v1.json"
PRICE_FILE = EXPORTS_DIR / "price_optimizer_v1.json"
TITLE_FILE = EXPORTS_DIR / "ai_title_optimizer_v1.json"
MULTI_FILE = EXPORTS_DIR / "multi_listing_generator_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "control_room_growth_status_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    performance = read_json(PERFORMANCE_FILE)
    price = read_json(PRICE_FILE)
    title = read_json(TITLE_FILE)
    multi = read_json(MULTI_FILE)

    performance_status = "MISSING"
    price_status = "MISSING"
    title_status = "MISSING"
    multi_status = "MISSING"
    optimized_title = ""
    recommended_price = 0.0

    if performance:
        performance_status = performance.get("performance_status", "MISSING")

    if price:
        price_status = price.get("optimizer_status", "MISSING")
        recommended_price = price.get("summary", {}).get("recommended_price", 0.0)

    if title:
        title_status = title.get("optimizer_status", "MISSING")
        optimized_title = title.get("summary", {}).get("optimized_title", "")

    if multi:
        multi_status = multi.get("generator_status", "MISSING")
        variant_count = multi.get("summary", {}).get("variant_count", 0)

    if performance_status == "READY" and price_status == "READY" and title_status == "READY" and multi_status == "READY":
        growth_status = "READY"
        next_step = "REVIEW_VARIANTS_AND_CHOOSE_EXECUTION_PATH"
    else:
        growth_status = "BLOCKED"
        next_step = "CHECK_OPTIMIZATION_LAYERS"

    output = {
        "growth_status": growth_status,
        "next_step": next_step,
        "summary": {
            "performance_status": performance_status,
            "price_status": price_status,
            "title_status": title_status,
            "multi_status": multi_status,
            "variant_count": variant_count,
            "recommended_price": recommended_price,
            "optimized_title": optimized_title
        },
        "inputs": {
            "performance_file": str(PERFORMANCE_FILE),
            "price_file": str(PRICE_FILE),
            "title_file": str(TITLE_FILE),
            "multi_file": str(MULTI_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("CONTROL_ROOM_GROWTH_STATUS_V1:")
    print("growth_status:", output["growth_status"])
    print("performance_status:", output["summary"]["performance_status"])
    print("price_status:", output["summary"]["price_status"])
    print("title_status:", output["summary"]["title_status"])
    print("multi_status:", output["summary"]["multi_status"])
    print("variant_count:", output["summary"]["variant_count"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
