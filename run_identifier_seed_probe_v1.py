import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def load_json(name):
    path = EXPORTS_DIR / name
    if not path.exists():
        return {"__missing__": True, "__file__": name}
    return json.loads(path.read_text(encoding="utf-8"))

def pick(data, keys):
    if not isinstance(data, dict):
        return None
    for k in keys:
        v = data.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None

def main():
    downstream = load_json("downstream_input_v1.json")
    inventory_mapper = load_json("inventory_full_payload_mapper_v1.json")
    inventory_probe = load_json("real_inventory_api_probe_v1.json")

    product_key = pick(downstream, ["product_key", "product_registry_key", "key"]) or pick(inventory_mapper, ["product_key", "product_registry_key", "key"]) or pick(inventory_probe, ["product_key", "product_registry_key", "key"])
    product_registry_key = pick(downstream, ["product_registry_key", "product_key"]) or pick(inventory_mapper, ["product_registry_key", "product_key"]) or pick(inventory_probe, ["product_registry_key", "product_key"])
    sku = pick(downstream, ["sku", "resolved_identifier", "identifier_value"]) or pick(inventory_mapper, ["sku", "resolved_identifier", "identifier_value"]) or pick(inventory_probe, ["sku", "resolved_identifier", "identifier_value"])
    inventory_item_key = pick(downstream, ["inventoryItemKey", "inventory_item_key"]) or pick(inventory_mapper, ["inventoryItemKey", "inventory_item_key"]) or pick(inventory_probe, ["inventoryItemKey", "inventory_item_key"])

    output = {
        "status": "OK",
        "decision": "identifier_seed_probe_v1_completed",
        "product_key": product_key,
        "product_registry_key": product_registry_key,
        "sku": sku,
        "inventory_item_key": inventory_item_key,
        "has_any_seed": bool(product_key or product_registry_key or sku or inventory_item_key),
        "next_step": "build_registry_lookup_call_v2_from_seed" if (product_key or product_registry_key or sku or inventory_item_key) else "inspect_upstream_mapper_outputs_for_missing_seed"
    }

    out_path = EXPORTS_DIR / "identifier_seed_probe_v1.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("IDENTIFIER_SEED_PROBE_V1_FINAL_AUDIT")
    print("status =", output["status"])
    print("decision =", output["decision"])
    print("product_key_present =", bool(output["product_key"]))
    print("product_registry_key_present =", bool(output["product_registry_key"]))
    print("sku_present =", bool(output["sku"]))
    print("inventory_item_key_present =", bool(output["inventory_item_key"]))
    print("has_any_seed =", output["has_any_seed"])
    print("next_step =", output["next_step"])

if __name__ == "__main__":
    main()
