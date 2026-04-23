import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "product_registry_identifier_resolution_probe_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "product_registry_lookup_call_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "product_registry_lookup_call_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    chosen_source = str(data.get("chosen_source") or "").strip()
    chosen_path = str(data.get("chosen_path") or "").strip()
    ready = bool(data.get("ready_for_registry_lookup"))
    result = {
        "status": "OK",
        "decision": "product_registry_lookup_call_v1_built",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "product_registry_lookup_call_version": "v1",
        "chosen_source": chosen_source,
        "chosen_path": chosen_path,
        "lookup_contract": {
            "call_type": "product_registry_lookup",
            "resolution_target": "live_inventory_identifier",
            "preferred_identifier_output": "sku"
        },
        "lookup_checks": {
            "source_is_product_registry_key": chosen_source == "product_registry_key",
            "path_is_read_first": chosen_path == "real_inventory_read_first",
            "ready_for_lookup_call": ready,
            "lookup_contract_present": True
        },
        "ready_for_registry_key_injection": ready and chosen_source == "product_registry_key" and chosen_path == "real_inventory_read_first",
        "next_step": "build_registry_key_injection_probe_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PRODUCT_REGISTRY_LOOKUP_CALL_V1_AUDIT")
    print("status = OK")
    print("decision = product_registry_lookup_call_v1_built")
    print("product_registry_lookup_call_version =", result["product_registry_lookup_call_version"])
    print("source_is_product_registry_key =", result["lookup_checks"]["source_is_product_registry_key"])
    print("path_is_read_first =", result["lookup_checks"]["path_is_read_first"])
    print("ready_for_lookup_call =", result["lookup_checks"]["ready_for_lookup_call"])
    print("lookup_contract_present =", result["lookup_checks"]["lookup_contract_present"])
    print("ready_for_registry_key_injection =", result["ready_for_registry_key_injection"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
