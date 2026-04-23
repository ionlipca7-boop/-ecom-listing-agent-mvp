import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
PIPELINE_STATUS_PATH = EXPORTS_DIR / "control_room_pipeline_status_v1.json" 
ALERT_STATE_PATH = EXPORTS_DIR / "control_room_alert_state_v1.json" 
OUTPUT_PATH = EXPORTS_DIR / "control_room_scheduler_gate_v1.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    pipeline = load_json(PIPELINE_STATUS_PATH) 
    alert = load_json(ALERT_STATE_PATH) 
 
    pipeline_status = pipeline.get("pipeline_status", "UNKNOWN") 
    final_decision = pipeline.get("final_decision", "UNKNOWN") 
    alert_state = alert.get("alert_state", "UNKNOWN") 
    actions_count = pipeline.get("actions_count", 0) 
 
    scheduler_action = "WAIT" 
    gate_reason = None 
 
    if str(pipeline_status).upper() == "READY_NEXT" and str(alert_state).upper() == "SEND_READY_NEXT": 
        scheduler_action = "RUN_NOW" 
        gate_reason = "ready_next_and_alert_present" 
    elif str(pipeline_status).upper() == "READY_BATCH" and str(alert_state).upper() == "SEND_READY_BATCH": 
        scheduler_action = "RUN_NOW" 
        gate_reason = "ready_batch_and_alert_present" 
    elif str(pipeline_status).upper() == "IDLE": 
        scheduler_action = "WAIT" 
        gate_reason = "pipeline_idle" 
    elif str(pipeline_status).upper() == "BLOCKED": 
        scheduler_action = "BLOCK" 
        gate_reason = "pipeline_blocked" 
    else: 
        scheduler_action = "BLOCK" 
        gate_reason = "unsupported_gate_state" 
 
    result = { 
        "status": "OK", 
        "pipeline_status": pipeline_status, 
        "final_decision": final_decision, 
        "alert_state": alert_state, 
        "actions_count": actions_count, 
        "scheduler_action": scheduler_action, 
        "gate_reason": gate_reason, 
        "paths": { 
            "pipeline_status_path": str(PIPELINE_STATUS_PATH), 
            "alert_state_path": str(ALERT_STATE_PATH), 
            "audit_path": str(OUTPUT_PATH) 
        } 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("CONTROL_ROOM_SCHEDULER_GATE_V1") 
    print("pipeline_status =", result["pipeline_status"]) 
    print("final_decision =", result["final_decision"]) 
    print("alert_state =", result["alert_state"]) 
    print("scheduler_action =", result["scheduler_action"]) 
    print("actions_count =", result["actions_count"]) 
    print("gate_reason =", result["gate_reason"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
