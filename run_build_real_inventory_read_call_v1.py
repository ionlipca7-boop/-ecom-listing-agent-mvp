import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "real_inventory_read_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "real_inventory_read_call_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "real_inventory_read_call_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    chosen_path = str(data.get("chosen_path") or "").strip()
    ready = bool(data.get("ready_for_real_inventory_read_call"))
    call = {
        "status": "OK",
        "decision": "real_inventory_read_call_v1_built",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "real_inventory_read_call_version": "v1",
        "chosen_path": chosen_path,
        "call_contract": {
            "call_type": "inventory_read",
            "mode": "real_api_read",
            "requires_live_identifier": True,
            "requires_token": True
        },
        "call_checks": {
            "path_is_read_first": chosen_path == "real_inventory_read_first",
            "ready_for_call_build": ready,
            "call_contract_present": True
        },
        "ready_for_live_inventory_identifier_injection": ready and chosen_path == "real_inventory_read_first",
        "next_step": "build_live_inventory_identifier_probe_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(call, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(call, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REAL_INVENTORY_READ_CALL_V1_AUDIT")
    print("status = OK")
    print("decision = real_inventory_read_call_v1_built")
    print("real_inventory_read_call_version =", call["real_inventory_read_call_version"])
    print("path_is_read_first =", call["call_checks"]["path_is_read_first"])
    print("ready_for_call_build =", call["call_checks"]["ready_for_call_build"])
    print("call_contract_present =", call["call_checks"]["call_contract_present"])
    print("ready_for_live_inventory_identifier_injection =", call["ready_for_live_inventory_identifier_injection"])
    print("next_step =", call["next_step"])

if __name__ == "__main__":
    main()
