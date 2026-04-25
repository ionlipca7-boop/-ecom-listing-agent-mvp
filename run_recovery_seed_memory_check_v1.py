import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
FILES = [
    "generator_output_contract_v2.json",
    "downstream_input_v1.json",
    "publish_payload_mapper_v1.json",
    "real_publish_mapper_v1.json",
    "inventory_full_payload_mapper_v1.json",
    "real_inventory_api_probe_v1.json"
]

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def find_first(obj, wanted):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in wanted and isinstance(v, str) and v.strip():
                return k, v.strip()
            found = find_first(v, wanted)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_first(item, wanted)
            if found:
                return found
    return None

def main():
    wanted_product = {"product_key", "product_registry_key", "key"}
    wanted_id = {"sku", "inventoryItemKey", "inventory_item_key", "identifier_value", "resolved_identifier"}
    found_product = None
    found_identifier = None
    found_product_file = "NONE"
    found_identifier_file = "NONE"

    for name in FILES:
        path = EXPORTS_DIR / name
        if not path.exists():
            continue
        data = load_json(path)
        if data is None:
            continue
        if not found_product:
            fp = find_first(data, wanted_product)
            if fp:
                found_product = fp
                found_product_file = name
        if not found_identifier:
            fi = find_first(data, wanted_id)
            if fi:
                found_identifier = fi
                found_identifier_file = name

    print("RECOVERY_SEED_MEMORY_CHECK_V1_FINAL_AUDIT")
    print("product_seed_found =", bool(found_product))
    print("product_seed_file =", found_product_file)
    print("product_seed_pair =", found_product if found_product else "NONE")
    print("identifier_seed_found =", bool(found_identifier))
    print("identifier_seed_file =", found_identifier_file)
    print("identifier_seed_pair =", found_identifier if found_identifier else "NONE")
    if found_product or found_identifier:
        print("next_step = build_registry_lookup_call_v2_from_recovered_seed")
    else:
        print("next_step = inspect_real_file_contents_of_verified_upstream_exports")

if __name__ == "__main__":
    main()
