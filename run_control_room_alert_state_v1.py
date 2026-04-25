import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
PIPELINE_STATUS_PATH = EXPORTS_DIR / "control_room_pipeline_status_v1.json" 
OUTPUT_PATH = EXPORTS_DIR / "control_room_alert_state_v1.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    pipeline = load_json(PIPELINE_STATUS_PATH) 
 
    pipeline_status = pipeline.get("pipeline_status", "UNKNOWN") 
    final_decision = pipeline.get("final_decision", "UNKNOWN") 
    actions_count = pipeline.get("actions_count", 0) 
    error_reason = pipeline.get("error_reason") 
 
    alert_state = "NO_ALERT" 
    alert_reason = None 
 
    if str(pipeline_status).upper() == "READY_NEXT": 
        alert_state = "SEND_READY_NEXT" 
        alert_reason = "pipeline_ready_for_next_step" 
    elif str(pipeline_status).upper() == "READY_BATCH": 
        alert_state = "SEND_READY_BATCH" 
        alert_reason = "pipeline_ready_for_batch" 
    elif str(pipeline_status).upper() == "IDLE": 
        alert_state = "NO_ALERT" 
        alert_reason = "pipeline_idle" 
    elif str(pipeline_status).upper() == "BLOCKED": 
        alert_state = "SEND_BLOCK_ALERT" 
        alert_reason = error_reason or "pipeline_blocked" 
    else: 
        alert_state = "SEND_BLOCK_ALERT" 
        alert_reason = "unknown_pipeline_state" 
 
    result = { 
        "status": "OK", 
        "pipeline_status": pipeline_status, 
        "final_decision": final_decision, 
        "actions_count": actions_count, 
        "alert_state": alert_state, 
        "alert_reason": alert_reason, 
        "source_path": str(PIPELINE_STATUS_PATH), 
        "audit_path": str(OUTPUT_PATH) 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("CONTROL_ROOM_ALERT_STATE_V1") 
    print("pipeline_status =", result["pipeline_status"]) 
    print("final_decision =", result["final_decision"]) 
    print("alert_state =", result["alert_state"]) 
    print("actions_count =", result["actions_count"]) 
    print("alert_reason =", result["alert_reason"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
