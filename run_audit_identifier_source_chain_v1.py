import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def load_json(name):
    path = EXPORTS_DIR / name
    if not path.exists():
        return {"__missing__": True, "__file__": name}
    return json.loads(path.read_text(encoding="utf-8"))

def short_value(v):
    if isinstance(v, str):
        s = v.strip()
        if len(s) > 120:
            return s[:120]
        return s
    return v

def get_candidates(data):
    keys = [
        "resolved_identifier", "identifier_value", "identifier", "sku",
        "inventoryItemKey", "inventory_item_key", "product_registry_key",
        "value", "key", "item_key"
    ]
    out = {}
    for k in keys:
        if isinstance(data, dict) and k in data:
            out[k] = short_value(data.get(k))
    return out

def first_real_string(candidates):
    for _, v in candidates.items():
        if isinstance(v, str) and v and v != "REPLACE_WITH_RESOLVED_LIVE_IDENTIFIER":
            return v
    return None

def main():
    registry_resolution = load_json("registry_resolution_call_v1.json")
    registry_lookup = load_json("product_registry_lookup_call_v1.json")
    resolution_stub = load_json("live_identifier_resolution_result_stub_v1.json")
    read_call_v1 = load_json("real_inventory_read_call_v1.json")

    rr_candidates = get_candidates(registry_resolution)
    rl_candidates = get_candidates(registry_lookup)
    rs_candidates = get_candidates(resolution_stub)
    rc_candidates = get_candidates(read_call_v1)

    best = first_real_string(rr_candidates) or first_real_string(rl_candidates) or first_real_string(rs_candidates) or first_real_string(rc_candidates)

    print("IDENTIFIER_SOURCE_CHAIN_V1_FINAL_AUDIT")
    print("registry_resolution_has_real_identifier =", bool(first_real_string(rr_candidates)))
    print("registry_lookup_has_real_identifier =", bool(first_real_string(rl_candidates)))
    print("resolution_stub_has_real_identifier =", bool(first_real_string(rs_candidates)))
    print("read_call_v1_has_real_identifier =", bool(first_real_string(rc_candidates)))
    print("best_identifier_found =", best if best else "NONE")
    print("registry_resolution_candidates =", rr_candidates)
    print("registry_lookup_candidates =", rl_candidates)
    print("resolution_stub_candidates =", rs_candidates)
    print("read_call_v1_candidates =", rc_candidates)

if __name__ == "__main__":
    main()
