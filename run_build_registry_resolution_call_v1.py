import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "registry_key_injection_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "registry_resolution_call_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "registry_resolution_call_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    chosen_source = str(data.get("chosen_source") or "").strip()
    chosen_path = str(data.get("chosen_path") or "").strip()
    ready = bool(data.get("ready_for_registry_resolution_call"))
    result = {
        "status": "OK",
        "decision": "registry_resolution_call_v1_built",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "registry_resolution_call_version": "v1",
        "chosen_source": chosen_source,
        "chosen_path": chosen_path,
        "resolution_call_contract": {
            "call_type": "registry_resolution",
            "input_identifier_type": "product_registry_key",
            "target_output_identifier": "sku",
            "target_usage": "live_inventory_read"
        },
        "call_checks": {
            "source_is_product_registry_key": chosen_source == "product_registry_key",
            "path_is_read_first": chosen_path == "real_inventory_read_first",
            "ready_for_resolution_call": ready,
            "resolution_call_contract_present": True
        },
        "ready_for_live_identifier_resolution_execution": ready and chosen_source == "product_registry_key" and chosen_path == "real_inventory_read_first",
        "next_step": "build_live_identifier_resolution_result_stub_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REGISTRY_RESOLUTION_CALL_V1_AUDIT")
    print("status = OK")
    print("decision = registry_resolution_call_v1_built")
    print("registry_resolution_call_version =", result["registry_resolution_call_version"])
    print("source_is_product_registry_key =", result["call_checks"]["source_is_product_registry_key"])
    print("path_is_read_first =", result["call_checks"]["path_is_read_first"])
    print("ready_for_resolution_call =", result["call_checks"]["ready_for_resolution_call"])
    print("resolution_call_contract_present =", result["call_checks"]["resolution_call_contract_present"])
    print("ready_for_live_identifier_resolution_execution =", result["ready_for_live_identifier_resolution_execution"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
