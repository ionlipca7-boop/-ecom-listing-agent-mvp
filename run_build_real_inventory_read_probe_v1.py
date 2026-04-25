import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "real_inventory_path_choice_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "real_inventory_read_probe_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "real_inventory_read_probe_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    chosen_path = str(data.get("chosen_path") or "").strip()
    ready = bool(data.get("ready_for_branching"))
    probe = {
        "status": "OK",
        "decision": "real_inventory_read_probe_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "real_inventory_read_probe_version": "v1",
        "chosen_path": chosen_path,
        "read_strategy": "read_live_inventory_before_full_update",
        "probe_checks": {
            "path_is_read_first": chosen_path == "real_inventory_read_first",
            "ready_for_read_probe": ready
        },
        "ready_for_real_inventory_read_call": ready and chosen_path == "real_inventory_read_first",
        "next_step": "build_real_inventory_read_call_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(probe, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REAL_INVENTORY_READ_PROBE_V1_AUDIT")
    print("status = OK")
    print("decision = real_inventory_read_probe_v1_completed")
    print("real_inventory_read_probe_version =", probe["real_inventory_read_probe_version"])
    print("path_is_read_first =", probe["probe_checks"]["path_is_read_first"])
    print("ready_for_read_probe =", probe["probe_checks"]["ready_for_read_probe"])
    print("ready_for_real_inventory_read_call =", probe["ready_for_real_inventory_read_call"])
    print("next_step =", probe["next_step"])

if __name__ == "__main__":
    main()
