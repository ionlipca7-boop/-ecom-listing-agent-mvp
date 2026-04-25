import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
PERFORMANCE_FILE = EXPORTS_DIR / "listing_performance_v1.json"
READY_FILE = EXPORTS_DIR / "real_ebay_template_export_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "price_optimizer_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def to_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0

def extract_price(data):
    if not data:
        return 0.0
    rows = data.get("rows", [])
    if not rows:
        return 0.0
    first_row = rows[0]
    return to_float(first_row.get("Price"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    performance = read_json(PERFORMANCE_FILE)
    ready_export = read_json(READY_FILE)

    performance_status = "MISSING"
    current_price = 0.0

    if performance:
        performance_status = performance.get("performance_status", "MISSING")

    current_price = extract_price(ready_export)

    recommended_price = current_price
    optimizer_status = "WAITING"
    strategy = "NO_CHANGE"
    next_step = "CHECK_PERFORMANCE_FIRST"

    if performance_status == "READY":
        optimizer_status = "READY"
        strategy = "BASELINE_PRICE_LOCK"
        next_step = "COLLECT_VIEWS_AND_SALES_BEFORE_PRICE_CHANGE"

    output = {
        "optimizer_status": optimizer_status,
        "strategy": strategy,
        "next_step": next_step,
        "summary": {
            "performance_status": performance_status,
            "current_price": current_price,
            "recommended_price": recommended_price,
            "currency": "EUR"
        },
        "rules": {
            "baseline_mode": "keep current price until real metrics arrive",
            "increase_trigger": "high views plus watchers plus low sales",
            "decrease_trigger": "high views plus zero sales after test window",
            "hold_trigger": "new listing without enough traffic data"
        },
        "inputs": {
            "performance_file": str(PERFORMANCE_FILE),
            "ready_file": str(READY_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("PRICE_OPTIMIZER_V1:")
    print("optimizer_status:", output["optimizer_status"])
    print("strategy:", output["strategy"])
    print("current_price:", output["summary"]["current_price"])
    print("recommended_price:", output["summary"]["recommended_price"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
