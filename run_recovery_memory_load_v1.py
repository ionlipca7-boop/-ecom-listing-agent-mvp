import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "recovery_memory_v1.json"
OUTPUT_PATH = EXPORTS_DIR / "recovery_memory_load_v1.json"

def main():
    data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    failures = data.get("known_failures", [])
    working_paths = data.get("working_paths", [])
    cmd_traps = data.get("cmd_traps", [])
    result = {
        "status": "OK",
        "decision": "recovery_memory_loaded",
        "memory_type": data.get("memory_type"),
        "failures_count": len(failures),
        "working_paths_count": len(working_paths),
        "cmd_traps_count": len(cmd_traps),
        "top_failure": failures[0] if failures else {},
        "top_working_path": working_paths[0] if working_paths else "",
        "top_cmd_trap": cmd_traps[0] if cmd_traps else ""
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("RECOVERY_MEMORY_LOAD_V1")
    print("failures_count =", len(failures))
    print("working_paths_count =", len(working_paths))
    print("cmd_traps_count =", len(cmd_traps))
    print("top_working_path =", working_paths[0] if working_paths else "")

if __name__ == "__main__":
    main()
