import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
MASTER_FILE = EXPORTS_DIR / "control_room_master_status_v1.json"
GROWTH_FILE = EXPORTS_DIR / "control_room_growth_status_v1.json"
EXECUTION_FILE = EXPORTS_DIR / "execution_control_room_v1.json"
PUBLISH_FILE = EXPORTS_DIR / "publish_variant_control_room_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "global_master_status_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    master_data = read_json(MASTER_FILE)
    growth_data = read_json(GROWTH_FILE)
    execution_data = read_json(EXECUTION_FILE)
    publish_data = read_json(PUBLISH_FILE)

    upload_status = "MISSING"
    growth_status = "MISSING"
    execution_status = "MISSING"
    publish_status = "MISSING"
    package_id = ""
    selected_variant_id = ""

    if master_data:
        upload_status = master_data.get("master_status", "MISSING")

    if growth_data:
        growth_status = growth_data.get("growth_status", "MISSING")

    if execution_data:
        execution_status = execution_data.get("execution_status", "MISSING")

    if publish_data:
        publish_status = publish_data.get("publish_variant_status", "MISSING")
        package_id = publish_data.get("summary", {}).get("package_id", "")
        selected_variant_id = publish_data.get("summary", {}).get("selected_variant_id", "")

    if growth_status == "READY" and execution_status == "READY" and publish_status == "READY":
        system_status = "READY"
        next_step = "READY_FOR_REAL_PUBLISH_OR_FINAL_HANDOFF"
    else:
        system_status = "BLOCKED"
        next_step = "CHECK_SUBSYSTEM_STATUS"

    output = {
        "system_status": system_status,
        "next_step": next_step,
        "summary": {
            "upload_status": upload_status,
            "growth_status": growth_status,
            "execution_status": execution_status,
            "publish_status": publish_status,
            "package_id": package_id,
            "selected_variant_id": selected_variant_id
        },
        "inputs": {
            "master_file": str(MASTER_FILE),
            "growth_file": str(GROWTH_FILE),
            "execution_file": str(EXECUTION_FILE),
            "publish_file": str(PUBLISH_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print("GLOBAL_MASTER_STATUS_V1:")
    print("system_status:", output["system_status"])
    print("upload_status:", output["summary"]["upload_status"])
    print("growth_status:", output["summary"]["growth_status"])
    print("execution_status:", output["summary"]["execution_status"])
    print("publish_status:", output["summary"]["publish_status"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
