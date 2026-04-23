import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
MASTER_STATUS_PATH = EXPORTS_DIR / "control_room_master_status_v2.json" 
AUTO_AGENT_V4_PATH = EXPORTS_DIR / "auto_agent_v4_audit.json" 
PIPELINE_STATUS_PATH = EXPORTS_DIR / "control_room_pipeline_status_v1.json" 
ALERT_STATE_PATH = EXPORTS_DIR / "control_room_alert_state_v1.json" 
OUTPUT_PATH = EXPORTS_DIR / "control_room_snapshot_v1.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    master = load_json(MASTER_STATUS_PATH) 
    agent = load_json(AUTO_AGENT_V4_PATH) 
    pipeline = load_json(PIPELINE_STATUS_PATH) 
    alert = load_json(ALERT_STATE_PATH) 
 
    result = { 
        "status": "OK", 
        "system_status": master.get("system_status"), 
        "overall_status": master.get("overall_status"), 
        "decision": master.get("decision"), 
        "last_execution_status": master.get("last_execution_status"), 
        "executor_returncode": master.get("executor_returncode"), 
        "actions_count": master.get("actions_count"), 
        "final_decision": agent.get("final_decision"), 
        "pipeline_status": pipeline.get("pipeline_status"), 
        "alert_state": alert.get("alert_state"), 
        "alert_reason": alert.get("alert_reason"), 
        "paths": { 
            "master_status_path": str(MASTER_STATUS_PATH), 
            "auto_agent_v4_path": str(AUTO_AGENT_V4_PATH), 
            "pipeline_status_path": str(PIPELINE_STATUS_PATH), 
            "alert_state_path": str(ALERT_STATE_PATH), 
            "audit_path": str(OUTPUT_PATH) 
        } 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("CONTROL_ROOM_SNAPSHOT_V1") 
    print("system_status =", result["system_status"]) 
    print("overall_status =", result["overall_status"]) 
    print("decision =", result["decision"]) 
    print("final_decision =", result["final_decision"]) 
    print("pipeline_status =", result["pipeline_status"]) 
    print("alert_state =", result["alert_state"]) 
    print("actions_count =", result["actions_count"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
