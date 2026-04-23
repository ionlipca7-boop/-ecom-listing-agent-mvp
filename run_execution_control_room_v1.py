import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
SELECTOR_FILE = EXPORTS_DIR / "variant_selector_v1.json"
EXECUTION_FILE = EXPORTS_DIR / "execution_variant_export_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "execution_control_room_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    selector_data = read_json(SELECTOR_FILE)
    execution_data = read_json(EXECUTION_FILE)

    selection_status = "MISSING"
    export_status = "MISSING"
    selected_variant_id = ""
    selected_title = ""
    selected_price = 0.0

    if selector_data:
        selection_status = selector_data.get("selection_status", "MISSING")
        selected_variant_id = selector_data.get("summary", {}).get("selected_variant_id", "")
        selected_title = selector_data.get("summary", {}).get("selected_title", "")
        selected_price = selector_data.get("summary", {}).get("selected_price", 0)

    if execution_data:
        export_status = execution_data.get("export_status", "MISSING")

    if selection_status == "READY" and export_status == "READY":
        execution_status = "READY"
        next_step = "READY_FOR_PUBLISH_PACKAGE_OR_NEXT_AGENT"
    else:
        execution_status = "BLOCKED"
        next_step = "CHECK_SELECTOR_OR_EXECUTION_EXPORT"

    output = {
        "execution_status": execution_status,
        "next_step": next_step,
        "summary": {
            "selection_status": selection_status,
            "export_status": export_status,
            "selected_variant_id": selected_variant_id,
            "selected_title": selected_title,
            "selected_price": selected_price
        },
        "inputs": {
            "selector_file": str(SELECTOR_FILE),
            "execution_file": str(EXECUTION_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print("EXECUTION_CONTROL_ROOM_V1:")
    print("execution_status:", output["execution_status"])
    print("selection_status:", output["summary"]["selection_status"])
    print("export_status:", output["summary"]["export_status"])
    print("selected_variant_id:", output["summary"]["selected_variant_id"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
