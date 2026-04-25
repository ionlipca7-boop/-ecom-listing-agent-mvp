import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "real_inventory_read_call_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "live_inventory_identifier_probe_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "live_inventory_identifier_probe_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    chosen_path = str(data.get("chosen_path") or "").strip()
    ready = bool(data.get("ready_for_live_inventory_identifier_injection"))
    result = {
        "status": "OK",
        "decision": "live_inventory_identifier_probe_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "live_inventory_identifier_probe_version": "v1",
        "chosen_path": chosen_path,
        "identifier_strategy": "inject_live_sku_or_inventory_item_group_key_before_real_read",
        "identifier_requirements": {
            "requires_live_identifier": True,
            "accepted_identifier_types": ["sku","inventory_item_group_key","product_registry_key"]
        },
        "probe_checks": {
            "path_is_read_first": chosen_path == "real_inventory_read_first",
            "ready_for_identifier_probe": ready,
            "identifier_requirements_present": True
        },
        "ready_for_live_identifier_resolution": ready and chosen_path == "real_inventory_read_first",
        "next_step": "choose_live_inventory_identifier_source_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("LIVE_INVENTORY_IDENTIFIER_PROBE_V1_AUDIT")
    print("status = OK")
    print("decision = live_inventory_identifier_probe_v1_completed")
    print("live_inventory_identifier_probe_version =", result["live_inventory_identifier_probe_version"])
    print("path_is_read_first =", result["probe_checks"]["path_is_read_first"])
    print("ready_for_identifier_probe =", result["probe_checks"]["ready_for_identifier_probe"])
    print("identifier_requirements_present =", result["probe_checks"]["identifier_requirements_present"])
    print("ready_for_live_identifier_resolution =", result["ready_for_live_identifier_resolution"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
