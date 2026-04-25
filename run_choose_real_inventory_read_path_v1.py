import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "real_inventory_api_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "real_inventory_path_choice_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "real_inventory_path_choice_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    ready = bool(data.get("ready_for_real_inventory_api_call"))
    result = {
        "status": "OK",
        "decision": "real_inventory_read_path_chosen",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "path_choice_version": "v1",
        "ready_for_branching": ready,
        "chosen_path": "real_inventory_read_first",
        "reason": "project_rule_read_live_first_then_build_full_update_payload",
        "next_step": "build_real_inventory_read_probe_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REAL_INVENTORY_PATH_CHOICE_V1_AUDIT")
    print("status = OK")
    print("decision = real_inventory_read_path_chosen")
    print("path_choice_version =", result["path_choice_version"])
    print("ready_for_branching =", result["ready_for_branching"])
    print("chosen_path =", result["chosen_path"])
    print("reason =", result["reason"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
