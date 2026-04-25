import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
PACKAGE_FILE = EXPORTS_DIR / "publish_package_from_variant_v1.json"
EXECUTION_FILE = EXPORTS_DIR / "execution_control_room_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "publish_variant_control_room_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    package_data = read_json(PACKAGE_FILE)
    execution_data = read_json(EXECUTION_FILE)

    package_status = "MISSING"
    execution_status = "MISSING"
    package_id = ""
    selected_variant_id = ""
    selected_title = ""

    if package_data:
        package_status = package_data.get("package_status", "MISSING")
        package_id = package_data.get("package_id", "")
        selected_variant_id = package_data.get("selected_variant_id", "")
        selected_title = package_data.get("selected_title", "")

    if execution_data:
        execution_status = execution_data.get("execution_status", "MISSING")

    if package_status == "READY" and execution_status == "READY":
        publish_variant_status = "READY"
        next_step = "READY_FOR_VARIANT_HANDOFF_OR_REAL_PUBLISH"
    else:
        publish_variant_status = "BLOCKED"
        next_step = "CHECK_PACKAGE_OR_EXECUTION_LAYER"

    output = {
        "publish_variant_status": publish_variant_status,
        "next_step": next_step,
        "summary": {
            "execution_status": execution_status,
            "package_status": package_status,
            "package_id": package_id,
            "selected_variant_id": selected_variant_id,
            "selected_title": selected_title
        },
        "inputs": {
            "package_file": str(PACKAGE_FILE),
            "execution_file": str(EXECUTION_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PUBLISH_VARIANT_CONTROL_ROOM_V1:")
    print("publish_variant_status:", output["publish_variant_status"])
    print("execution_status:", output["summary"]["execution_status"])
    print("package_status:", output["summary"]["package_status"])
    print("package_id:", output["summary"]["package_id"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
