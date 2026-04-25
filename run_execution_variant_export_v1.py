import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
READY_FILE = EXPORTS_DIR / "real_ebay_template_export_v1.json"
SELECTOR_FILE = EXPORTS_DIR / "variant_selector_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "execution_variant_export_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def get_first_row(data):
    if not data:
        return None
    rows = data.get("rows", [])
    if not rows:
        return None
    return rows[0]

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ready_data = read_json(READY_FILE)
    selector_data = read_json(SELECTOR_FILE)
    row = get_first_row(ready_data)
    selected_variant = None
    export_status = "WAITING"
    next_step = "CHECK_SELECTOR_FIRST"
    execution_payload = {}

    if selector_data:
        selected_variant = selector_data.get("selected_variant")

    if row and selected_variant:
        execution_payload = dict(row)
        execution_payload["Title"] = selected_variant.get("title", row.get("Title", ""))
        execution_payload["Price"] = selected_variant.get("price", row.get("Price", 0))
        execution_payload["SelectedVariantID"] = selected_variant.get("variant_id", "")
        execution_payload["SelectedAngle"] = selected_variant.get("angle", "")
        execution_payload["ExecutionSource"] = "execution_variant_export_v1"
        export_status = "READY"
        next_step = "READY_FOR_EXECUTION_OR_PUBLISH_LAYER"

    selected_variant_id = ""
    selected_title = ""
    selected_price = 0.0

    if selected_variant:
        selected_variant_id = selected_variant.get("variant_id", "")
        selected_title = selected_variant.get("title", "")
        selected_price = selected_variant.get("price", 0)

    output = {
        "export_status": export_status,
        "next_step": next_step,
        "summary": {
            "selected_variant_id": selected_variant_id,
            "selected_title": selected_title,
            "selected_price": selected_price
        },
        "execution_payload": execution_payload,
        "inputs": {
            "ready_file": str(READY_FILE),
            "selector_file": str(SELECTOR_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print("EXECUTION_VARIANT_EXPORT_V1:")
    print("export_status:", output["export_status"])
    print("selected_variant_id:", output["summary"]["selected_variant_id"])
    print("selected_title:", output["summary"]["selected_title"])
    print("selected_price:", output["summary"]["selected_price"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
