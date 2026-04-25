import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
READY_FILE = EXPORTS_DIR / "fixed_reupload_ready_status_v1.json"
PREP_FILE = EXPORTS_DIR / "fixed_reupload_prep_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "manual_fixed_reupload_handoff_v1.json"

def read_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")

def main():
    ready = read_json(READY_FILE)
    prep = read_json(PREP_FILE)
    ready_status = ready.get("ready_status", "")
    ready_gate = ready.get("ready_gate", "")
    payload_complete = ready.get("payload_complete", "NO")
    export_fields = ready.get("export_fields", [])
    reupload_payload = prep.get("reupload_payload", {})
    checklist = []
    checklist.append("Открыть актуальный fixed package или listing draft для повторной загрузки")
    checklist.append("Проверить Brand, item specifics и price перед повторной загрузкой")
    checklist.append("Запустить повторную ручную загрузку в eBay")
    checklist.append("Сохранить новый upload result JSON для следующего parser cycle")
    checklist.append("После повторной загрузки прогнать parser и compare result")
    if ready_status == "READY" and ready_gate == "OPEN" and payload_complete == "YES":
        handoff_status = "READY"
        handoff_gate = "OPEN"
        next_step = "DO_MANUAL_FIXED_REUPLOAD"
    elif ready_status == "READY":
        handoff_status = "PARTIAL"
        handoff_gate = "REVIEW"
        next_step = "REVIEW_MANUAL_HANDOFF_BEFORE_REUPLOAD"
    else:
        handoff_status = "BLOCKED"
        handoff_gate = "CLOSED"
        next_step = "RETURN_TO_READY_STATUS_LAYER"
    output = {}
    output["handoff_status"] = handoff_status
    output["handoff_gate"] = handoff_gate
    output["next_step"] = next_step
    output["ready_status"] = ready_status
    output["ready_gate"] = ready_gate
    output["payload_complete"] = payload_complete
    output["export_fields"] = export_fields
    output["reupload_payload"] = reupload_payload
    output["manual_checklist"] = checklist
    output["source_files"] = {}
    output["source_files"]["fixed_reupload_ready_status"] = str(READY_FILE)
    output["source_files"]["fixed_reupload_prep"] = str(PREP_FILE)
    write_json(OUTPUT_FILE, output)
    print("MANUAL_FIXED_REUPLOAD_HANDOFF_V1:")
    print("handoff_status:", handoff_status)
    print("handoff_gate:", handoff_gate)
    print("payload_complete:", payload_complete)
    print("next_step:", next_step)
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
