import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
 
STATUS_PATH = EXPORTS_DIR / "control_room_status_v1.json" 
MASTER_V1_PATH = EXPORTS_DIR / "control_room_master_status_v1.json" 
AUTO_AGENT_V2_PATH = EXPORTS_DIR / "auto_agent_v2_audit.json" 
BATCH_PATH = EXPORTS_DIR / "batch_actions_v1_audit.json" 
AUTO_AGENT_V3_PATH = EXPORTS_DIR / "auto_agent_v3_audit.json" 
ACTION_PATH = EXPORTS_DIR / "control_action_v5.json" 
OUTPUT_PATH = EXPORTS_DIR / "control_room_master_status_v2.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    status_data = load_json(STATUS_PATH) 
    master_v1_data = load_json(MASTER_V1_PATH) 
    auto_agent_v2_data = load_json(AUTO_AGENT_V2_PATH) 
    batch_data = load_json(BATCH_PATH) 
    auto_agent_v3_data = load_json(AUTO_AGENT_V3_PATH) 
    action_data = load_json(ACTION_PATH) 
 
    system_status = status_data.get("system_status", "UNKNOWN") 
    decision = auto_agent_v3_data.get("decision", "UNKNOWN") 
    actions_count = auto_agent_v3_data.get("actions_count") 
    if actions_count is None: 
        actions_count = batch_data.get("actions_count") 
    if actions_count is None: 
        actions_count = auto_agent_v2_data.get("actions_count", 0) 
 
    last_execution_status = action_data.get("result_status") 
    if last_execution_status is None: 
        last_execution_status = action_data.get("status", "UNKNOWN") 
 
    executor_returncode = action_data.get("executor_returncode") 
    if executor_returncode is None: 
        executor_returncode = 1 
        if str(last_execution_status).upper() == "OK": 
            executor_returncode = 0 
 
    checks = [ 
        ("system_status", system_status), 
        ("master_v1", master_v1_data.get("overall_status", master_v1_data.get("status", "UNKNOWN"))), 
        ("auto_agent_v2", auto_agent_v2_data.get("status", "UNKNOWN")), 
        ("batch_actions_v1", batch_data.get("status", "UNKNOWN")), 
        ("auto_agent_v3", auto_agent_v3_data.get("status", "UNKNOWN")), 
        ("control_action_v5", last_execution_status), 
    ] 
 
    error_reason = None 
    for name, value in checks: 
        if str(value).upper() != "OK": 
            error_reason = name + ":" + str(value) 
            break 
 
    overall_status = "OK" 
    if error_reason is not None: 
        overall_status = "ERROR" 
 
    result = { 
        "status": "OK", 
        "system_status": system_status, 
        "overall_status": overall_status, 
        "actions_count": actions_count, 
        "decision": decision, 
        "last_execution_status": last_execution_status, 
        "executor_returncode": executor_returncode, 
        "paths": { 
            "status_path": str(STATUS_PATH), 
            "action_path": str(ACTION_PATH), 
            "audit_path": str(OUTPUT_PATH) 
        }, 
        "error_reason": error_reason 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("CONTROL_ROOM_MASTER_STATUS_V2") 
    print("system_status =", result["system_status"]) 
    print("overall_status =", result["overall_status"]) 
    print("actions_count =", result["actions_count"]) 
    print("decision =", result["decision"]) 
    print("last_execution_status =", result["last_execution_status"]) 
    print("executor_returncode =", result["executor_returncode"]) 
    print("error_reason =", result["error_reason"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
