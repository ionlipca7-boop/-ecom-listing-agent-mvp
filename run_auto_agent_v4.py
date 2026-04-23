import json 
from pathlib import Path 
 
BASE_DIR = Path(__file__).resolve().parent 
EXPORTS_DIR = BASE_DIR / "storage" / "exports" 
MASTER_STATUS_PATH = EXPORTS_DIR / "control_room_master_status_v2.json" 
OUTPUT_PATH = EXPORTS_DIR / "auto_agent_v4_audit.json" 
 
def load_json(path): 
    if not path.exists(): 
        return {"status": "ERROR", "error_reason": "missing_file:" + path.name} 
    return json.loads(path.read_text(encoding="utf-8")) 
 
def main(): 
    master = load_json(MASTER_STATUS_PATH) 
 
    overall_status = master.get("overall_status", "UNKNOWN") 
    decision = master.get("decision", "UNKNOWN") 
    last_execution_status = master.get("last_execution_status", "UNKNOWN") 
    actions_count = master.get("actions_count", 0) 
    executor_returncode = master.get("executor_returncode", 1) 
 
    final_decision = "BLOCK" 
    error_reason = None 
 
    if str(overall_status).upper() != "OK": 
        final_decision = "BLOCK" 
        error_reason = "overall_status_not_ok" 
    elif str(decision).upper() == "SKIP": 
        final_decision = "SKIP" 
    elif str(decision).upper() == "RUN_SINGLE" and str(last_execution_status).upper() == "OK": 
        final_decision = "READY_NEXT" 
    elif str(decision).upper() == "RUN_BATCH" and str(last_execution_status).upper() == "OK": 
        final_decision = "READY_BATCH" 
    else: 
        final_decision = "BLOCK" 
        error_reason = "unsupported_state" 
 
    result = { 
        "status": "OK", 
        "input_status": overall_status, 
        "input_decision": decision, 
        "last_execution_status": last_execution_status, 
        "executor_returncode": executor_returncode, 
        "actions_count": actions_count, 
        "final_decision": final_decision, 
        "error_reason": error_reason, 
        "source_path": str(MASTER_STATUS_PATH), 
        "audit_path": str(OUTPUT_PATH) 
    } 
 
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8") 
 
    print("AUTO_AGENT_V4") 
    print("input_status =", result["input_status"]) 
    print("input_decision =", result["input_decision"]) 
    print("final_decision =", result["final_decision"]) 
    print("actions_count =", result["actions_count"]) 
    print("error_reason =", result["error_reason"]) 
    print("output_file =", OUTPUT_PATH) 
 
if __name__ == "__main__": 
    main() 
