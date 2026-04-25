import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def load_json(name):
    path = EXPORTS_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))

def pick_identifier_value(data):
    candidates = [
        data.get("resolved_identifier"),
        data.get("identifier_value"),
        data.get("sku"),
        data.get("inventoryItemKey"),
        data.get("inventory_item_key"),
        data.get("product_registry_key"),
    ]
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "REPLACE_WITH_RESOLVED_LIVE_IDENTIFIER"

def main():
    resolution_call = load_json("registry_resolution_call_v1.json")
    identifier_type = resolution_call.get("identifier_type") or "sku"
    identifier_value = pick_identifier_value(resolution_call)

    output = {
        "status": "OK",
        "decision": "live_identifier_resolution_result_v1_created",
        "identifier_source": "registry_resolution_call_v1",
        "identifier_type": identifier_type,
        "identifier_value": identifier_value,
        "resolved_ok": identifier_value != "REPLACE_WITH_RESOLVED_LIVE_IDENTIFIER",
        "next_step": "rebuild_real_inventory_read_call_v2_with_real_identifier"
    }

    out_path = EXPORTS_DIR / "live_identifier_resolution_result_v1.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
