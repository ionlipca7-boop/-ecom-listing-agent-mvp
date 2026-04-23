import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
SNAPSHOT_PATH = EXPORTS_DIR / "control_room_snapshot_v1.json" 
MESSAGE_PATH = EXPORTS_DIR / "control_room_message_payload_v1.json" 
SCHEDULER_PATH = EXPORTS_DIR / "control_room_scheduler_gate_v1.json" 
OUTPUT_PATH = EXPORTS_DIR / "control_room_delivery_packet_v1.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    snapshot = load_json(SNAPSHOT_PATH) 
    message = load_json(MESSAGE_PATH) 
    scheduler = load_json(SCHEDULER_PATH) 
 
    pipeline_status = snapshot.get("pipeline_status", "UNKNOWN") 
    alert_state = snapshot.get("alert_state", "UNKNOWN") 
    actions_count = snapshot.get("actions_count", 0) 
    message_type = message.get("message_type", "UNKNOWN") 
    title = message.get("title", "UNKNOWN") 
    message_text = message.get("message_text", "") 
    scheduler_action = scheduler.get("scheduler_action", "UNKNOWN") 
    gate_reason = scheduler.get("gate_reason") 
 
    delivery_status = "BLOCKED" 
    delivery_action = "DO_NOT_SEND" 
    error_reason = None 
 
    if str(scheduler_action).upper() == "RUN_NOW": 
        delivery_status = "READY" 
        delivery_action = "SEND_NOW" 
    elif str(scheduler_action).upper() == "WAIT": 
        delivery_status = "WAITING" 
        delivery_action = "QUEUE" 
    elif str(scheduler_action).upper() == "BLOCK": 
        delivery_status = "BLOCKED" 
        delivery_action = "DO_NOT_SEND" 
        error_reason = gate_reason or "scheduler_blocked" 
    else: 
        delivery_status = "BLOCKED" 
        delivery_action = "DO_NOT_SEND" 
        error_reason = "unsupported_scheduler_action" 
 
    result = { 
        "status": "OK", 
        "delivery_status": delivery_status, 
        "delivery_action": delivery_action, 
        "pipeline_status": pipeline_status, 
        "alert_state": alert_state, 
        "scheduler_action": scheduler_action, 
        "message_type": message_type, 
        "title": title, 
        "message_text": message_text, 
        "actions_count": actions_count, 
        "gate_reason": gate_reason, 
        "error_reason": error_reason, 
        "paths": { 
            "snapshot_path": str(SNAPSHOT_PATH), 
            "message_path": str(MESSAGE_PATH), 
            "scheduler_path": str(SCHEDULER_PATH), 
            "audit_path": str(OUTPUT_PATH) 
        } 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("CONTROL_ROOM_DELIVERY_PACKET_V1") 
    print("delivery_status =", result["delivery_status"]) 
    print("delivery_action =", result["delivery_action"]) 
    print("scheduler_action =", result["scheduler_action"]) 
    print("message_type =", result["message_type"]) 
    print("actions_count =", result["actions_count"]) 
    print("error_reason =", result["error_reason"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
