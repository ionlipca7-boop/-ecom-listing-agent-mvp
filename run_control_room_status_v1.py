import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
REGISTRY_PATH = EXPORTS_DIR / "products_registry_v1.json"
ACTION_PATH = EXPORTS_DIR / "control_action_v4.json"
RESOLVE_PATH = EXPORTS_DIR / "registry_resolve_action_v1_audit.json"
EXECUTION_PATH = EXPORTS_DIR / "control_action_v5.json"
RESULT_PATH = EXPORTS_DIR / "control_room_status_v1.json"
def safe_load(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
def main():
    registry = safe_load(REGISTRY_PATH)
    action = safe_load(ACTION_PATH)
    resolve = safe_load(RESOLVE_PATH)
    execution = safe_load(EXECUTION_PATH)
    registry_ok = bool(registry and registry.get("products"))
    action_ok = bool(action and action.get("actions"))
    resolve_ok = bool(resolve and resolve.get("status") == "OK")
    execution_ok = bool(execution and execution.get("status") == "OK")
    if registry_ok and action_ok and resolve_ok and execution_ok:
        system_status = "OK"
    elif registry_ok or action_ok or resolve_ok or execution_ok:
        system_status = "PARTIAL"
    else:
        system_status = "FAILED"
    result = {
        "system_status": system_status,
        "registry_ok": registry_ok,
        "action_ok": action_ok,
        "resolve_ok": resolve_ok,
        "execution_ok": execution_ok,
        "paths": {
            "registry": str(REGISTRY_PATH),
            "action": str(ACTION_PATH),
            "resolve": str(RESOLVE_PATH),
            "execution": str(EXECUTION_PATH)
        }
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CONTROL_ROOM_STATUS_V1")
    print("system_status =", system_status)
    print("registry_ok =", registry_ok)
    print("action_ok =", action_ok)
    print("resolve_ok =", resolve_ok)
    print("execution_ok =", execution_ok)
    print("result_file =", RESULT_PATH)
if __name__ == "__main__":
    main()
