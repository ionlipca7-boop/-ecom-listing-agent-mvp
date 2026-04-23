import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

STATUS_PATH = EXPORTS_DIR / "control_room_status_v1.json"
AUTO_V2_PATH = EXPORTS_DIR / "auto_agent_v2_audit.json"
BATCH_PATH = EXPORTS_DIR / "batch_actions_v1_audit.json"
AUTO_V3_PATH = EXPORTS_DIR / "auto_agent_v3_audit.json"
OUTPUT_PATH = EXPORTS_DIR / "control_room_master_status_v1.json"

def load_json(path):
    if not path.exists():
        return {"status": "NOT_FOUND"}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return {"status": "INVALID_JSON"}

def main():
    status_data = load_json(STATUS_PATH)
    auto_v2 = load_json(AUTO_V2_PATH)
    batch = load_json(BATCH_PATH)
    auto_v3 = load_json(AUTO_V3_PATH)

    system_status = status_data.get("system_status", "UNKNOWN")
    auto_v2_status = auto_v2.get("status", "UNKNOWN")
    batch_status = batch.get("status", "UNKNOWN")
    auto_v3_status = auto_v3.get("status", "UNKNOWN")

    all_ok = (
        system_status == "OK" and
        auto_v2_status == "OK" and
        batch_status == "OK" and
        auto_v3_status == "OK"
    )

    overall_status = "OK" if all_ok else "PARTIAL"

    result = {
        "system_status": system_status,
        "auto_agent_v2": auto_v2_status,
        "batch_actions_v1": batch_status,
        "auto_agent_v3": auto_v3_status,
        "overall_status": overall_status
    }

    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("CONTROL_ROOM_MASTER_STATUS_V1")
    print("system_status =", system_status)
    print("auto_agent_v2 =", auto_v2_status)
    print("batch_actions_v1 =", batch_status)
    print("auto_agent_v3 =", auto_v3_status)
    print("overall_status =", overall_status)
    print("output_file =", OUTPUT_PATH)

if __name__ == "__main__":
    main()
