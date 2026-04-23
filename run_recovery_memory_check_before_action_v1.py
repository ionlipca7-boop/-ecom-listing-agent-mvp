import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "recovery_memory_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "recovery_memory_check_before_action_v1.json"

def main():
    action_name = sys.argv[1].strip() if len(sys.argv) > 1 else "unknown_action"
    memory = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    failures = memory.get("known_failures", [])
    working_paths = memory.get("working_paths", [])
    cmd_traps = memory.get("cmd_traps", [])
    action_low = action_name.lower()
    matched_failures = []
    recommended_working_paths = []
    recommended_cmd_traps = []

    for item in failures:
        text = json.dumps(item, ensure_ascii=False).lower()
        if "token" in action_low and "token" in text:
            matched_failures.append(item)
        elif "offer" in action_low and ("sku" in text or "inventory" in text or "content-language" in text):
            matched_failures.append(item)
        elif "inventory" in action_low and ("inventory" in text or "sku" in text):
            matched_failures.append(item)
        elif "policy" in action_low and ("token" in text):
            matched_failures.append(item)

    for item in working_paths:
        low = item.lower()
        if "token" in action_low and ("oauth" in low or "refresh" in low or "smoke test" in low):
            recommended_working_paths.append(item)
        elif "offer" in action_low and ("payload" in low or "policy" in low or "category" in low):
            recommended_working_paths.append(item)
        elif "inventory" in action_low and ("payload" in low or "smoke test" in low):
            recommended_working_paths.append(item)

    for item in cmd_traps:
        if item not in recommended_cmd_traps:
            recommended_cmd_traps.append(item)

    result = {
        "status": "OK",
        "decision": "pre_action_memory_check_completed",
        "action_name": action_name,
        "matched_failures_count": len(matched_failures),
        "recommended_working_paths_count": len(recommended_working_paths),
        "matched_failures": matched_failures,
        "recommended_working_paths": recommended_working_paths,
        "recommended_cmd_traps": recommended_cmd_traps[:5]
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("RECOVERY_MEMORY_CHECK_BEFORE_ACTION_V1")
    print("action_name =", action_name)
    print("matched_failures_count =", len(matched_failures))
    print("recommended_working_paths_count =", len(recommended_working_paths))

if __name__ == "__main__":
    main()
