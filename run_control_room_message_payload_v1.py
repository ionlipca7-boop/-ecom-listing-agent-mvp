import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
SNAPSHOT_PATH = EXPORTS_DIR / "control_room_snapshot_v1.json" 
OUTPUT_PATH = EXPORTS_DIR / "control_room_message_payload_v1.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    snapshot = load_json(SNAPSHOT_PATH) 
 
    system_status = snapshot.get("system_status", "UNKNOWN") 
    overall_status = snapshot.get("overall_status", "UNKNOWN") 
    final_decision = snapshot.get("final_decision", "UNKNOWN") 
    pipeline_status = snapshot.get("pipeline_status", "UNKNOWN") 
    alert_state = snapshot.get("alert_state", "UNKNOWN") 
    actions_count = snapshot.get("actions_count", 0) 
    alert_reason = snapshot.get("alert_reason") 
 
    message_type = "INFO" 
    title = "CONTROL ROOM UPDATE" 
 
    if str(alert_state).upper() == "SEND_READY_NEXT": 
        message_type = "READY_NEXT" 
        title = "CONTROL ROOM READY NEXT" 
    elif str(alert_state).upper() == "SEND_READY_BATCH": 
        message_type = "READY_BATCH" 
        title = "CONTROL ROOM READY BATCH" 
    elif str(alert_state).upper() == "SEND_BLOCK_ALERT": 
        message_type = "BLOCK_ALERT" 
        title = "CONTROL ROOM BLOCKED" 
 
    message_text = "system_status=" + str(system_status) + "; overall_status=" + str(overall_status) + "; final_decision=" + str(final_decision) + "; pipeline_status=" + str(pipeline_status) + "; alert_state=" + str(alert_state) + "; actions_count=" + str(actions_count) + "; alert_reason=" + str(alert_reason) 
 
    result = { 
        "status": "OK", 
        "message_type": message_type, 
        "title": title, 
        "message_text": message_text, 
        "pipeline_status": pipeline_status, 
        "alert_state": alert_state, 
        "actions_count": actions_count, 
        "source_path": str(SNAPSHOT_PATH), 
        "audit_path": str(OUTPUT_PATH) 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("CONTROL_ROOM_MESSAGE_PAYLOAD_V1") 
    print("message_type =", result["message_type"]) 
    print("title =", result["title"]) 
    print("pipeline_status =", result["pipeline_status"]) 
    print("alert_state =", result["alert_state"]) 
    print("actions_count =", result["actions_count"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
