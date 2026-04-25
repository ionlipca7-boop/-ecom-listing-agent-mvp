import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "live_inventory_identifier_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "live_inventory_identifier_source_choice_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "live_inventory_identifier_source_choice_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    ready = bool(data.get("ready_for_live_identifier_resolution"))
    chosen_path = str(data.get("chosen_path") or "").strip()
    result = {
        "status": "OK",
        "decision": "live_inventory_identifier_source_v1_chosen",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "identifier_source_choice_version": "v1",
        "chosen_path": chosen_path,
        "source_priority": ["product_registry_key","sku","inventory_item_group_key"],
        "chosen_source": "product_registry_key",
        "reason": "project_prefers_registry_first_for_control_room_resolution",
        "choice_checks": {
            "ready_for_source_choice": ready,
            "path_is_read_first": chosen_path == "real_inventory_read_first",
            "source_priority_present": True
        },
        "ready_for_registry_resolution_probe": ready and chosen_path == "real_inventory_read_first",
        "next_step": "build_product_registry_identifier_resolution_probe_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("LIVE_INVENTORY_IDENTIFIER_SOURCE_CHOICE_V1_AUDIT")
    print("status = OK")
    print("decision = live_inventory_identifier_source_v1_chosen")
    print("identifier_source_choice_version =", result["identifier_source_choice_version"])
    print("ready_for_source_choice =", result["choice_checks"]["ready_for_source_choice"])
    print("path_is_read_first =", result["choice_checks"]["path_is_read_first"])
    print("chosen_source =", result["chosen_source"])
    print("ready_for_registry_resolution_probe =", result["ready_for_registry_resolution_probe"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
