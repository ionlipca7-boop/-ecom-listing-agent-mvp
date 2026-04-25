import json
from pathlib import Path
ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
EXPORTS = ROOT / "storage" / "exports"
p = EXPORTS / "first_real_multi_listing_run_payload_v4.json"
d = json.loads(p.read_text(encoding="utf-8"))
print("MULTI_LISTING_STRUCTURE_AUDIT_V1")
print("root_keys =", list(d.keys()))
for k, v in d.items():
    print("---", k, "---")
    print("type =", type(v).__name__)
    if isinstance(v, dict):
        print("len =", len(v))
        print("keys =", list(v.keys()))
    elif isinstance(v, list):
        print("len =", len(v))
        if len(v) > 0 and isinstance(v[0], dict):
            print("first_item_keys =", list(v[0].keys()))
        else:
            print("value =", v)
    else:
        print("value =", v)
print("next_step = locate_real_inventory_and_offer_payload_sources")
