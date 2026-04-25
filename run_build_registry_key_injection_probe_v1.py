import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / "storage" / "exports" / "product_registry_lookup_call_v1.json"
OUT = BASE_DIR / "storage" / "exports" / "registry_key_injection_probe_v1.json"
ARCH = BASE_DIR / "storage" / "memory" / "archive" / "registry_key_injection_probe_v1_2026_04_18.json"

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    chosen_source = str(data.get("chosen_source") or "").strip()
    chosen_path = str(data.get("chosen_path") or "").strip()
    ready = bool(data.get("ready_for_registry_key_injection"))
    result = {
        "status": "OK",
        "decision": "registry_key_injection_probe_v1_completed",
        "source_file": str(SRC.relative_to(BASE_DIR)).replace("/", "\\"),
        "registry_key_injection_probe_version": "v1",
        "chosen_source": chosen_source,
        "chosen_path": chosen_path,
        "injection_strategy": "inject_product_registry_key_into_registry_resolution_flow",
        "probe_checks": {
            "source_is_product_registry_key": chosen_source == "product_registry_key",
            "path_is_read_first": chosen_path == "real_inventory_read_first",
            "ready_for_injection_probe": ready
        },
        "ready_for_registry_resolution_call": ready and chosen_source == "product_registry_key" and chosen_path == "real_inventory_read_first",
        "next_step": "build_registry_resolution_call_v1"
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ARCH.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    ARCH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("REGISTRY_KEY_INJECTION_PROBE_V1_AUDIT")
    print("status = OK")
    print("decision = registry_key_injection_probe_v1_completed")
    print("registry_key_injection_probe_version =", result["registry_key_injection_probe_version"])
    print("source_is_product_registry_key =", result["probe_checks"]["source_is_product_registry_key"])
    print("path_is_read_first =", result["probe_checks"]["path_is_read_first"])
    print("ready_for_injection_probe =", result["probe_checks"]["ready_for_injection_probe"])
    print("ready_for_registry_resolution_call =", result["ready_for_registry_resolution_call"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
