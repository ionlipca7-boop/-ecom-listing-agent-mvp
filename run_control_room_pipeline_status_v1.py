import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
MASTER_STATUS_PATH = EXPORTS_DIR / "control_room_master_status_v2.json" 
AUTO_AGENT_V4_PATH = EXPORTS_DIR / "auto_agent_v4_audit.json" 
OUTPUT_PATH = EXPORTS_DIR / "control_room_pipeline_status_v1.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    master = load_json(MASTER_STATUS_PATH) 
    agent = load_json(AUTO_AGENT_V4_PATH) 
 
    overall_status = master.get("overall_status", "UNKNOWN") 
    system_status = master.get("system_status", "UNKNOWN") 
    input_decision = master.get("decision", "UNKNOWN") 
    final_decision = agent.get("final_decision", "UNKNOWN") 
    actions_count = master.get("actions_count", 0) 
    last_execution_status = master.get("last_execution_status", "UNKNOWN") 
    executor_returncode = master.get("executor_returncode", 1) 
 
    pipeline_status = "BLOCKED" 
    error_reason = None 
 
    if str(overall_status).upper() != "OK": 
        pipeline_status = "BLOCKED" 
        error_reason = "overall_status_not_ok" 
    elif str(final_decision).upper() == "READY_NEXT": 
        pipeline_status = "READY_NEXT" 
    elif str(final_decision).upper() == "READY_BATCH": 
        pipeline_status = "READY_BATCH" 
    elif str(final_decision).upper() == "SKIP": 
        pipeline_status = "IDLE" 
    else: 
        pipeline_status = "BLOCKED" 
        error_reason = "unsupported_pipeline_state" 
 
    result = { 
        "status": "OK", 
        "system_status": system_status, 
        "overall_status": overall_status, 
        "input_decision": input_decision, 
        "final_decision": final_decision, 
        "pipeline_status": pipeline_status, 
        "actions_count": actions_count, 
        "last_execution_status": last_execution_status, 
        "executor_returncode": executor_returncode, 
        "error_reason": error_reason, 
        "paths": { 
            "master_status_path": str(MASTER_STATUS_PATH), 
            "auto_agent_v4_path": str(AUTO_AGENT_V4_PATH), 
            "audit_path": str(OUTPUT_PATH) 
        } 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("CONTROL_ROOM_PIPELINE_STATUS_V1") 
    print("system_status =", result["system_status"]) 
    print("overall_status =", result["overall_status"]) 
    print("final_decision =", result["final_decision"]) 
    print("pipeline_status =", result["pipeline_status"]) 
    print("actions_count =", result["actions_count"]) 
    print("error_reason =", result["error_reason"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
