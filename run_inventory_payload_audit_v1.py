import json
from pathlib import Path
ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
EXPORTS = ROOT / "storage" / "exports"
p = EXPORTS / "first_real_multi_listing_run_payload_v4.json"
d = json.loads(p.read_text(encoding="utf-8"))
inv = d.get("inventory_payload")
print("INVENTORY_PAYLOAD_AUDIT_V1")
print("inventory_payload_is_dict =", isinstance(inv, dict))
print("inventory_payload_len =", len(inv) if isinstance(inv, dict) else -1)
print("inventory_payload_keys =", list(inv.keys()) if isinstance(inv, dict) else [])
print("sku =", inv.get("sku") if isinstance(inv, dict) else None)
print("has_product =", "product" in inv if isinstance(inv, dict) else False)
print("has_availability =", "availability" in inv if isinstance(inv, dict) else False)
print("has_condition =", "condition" in inv if isinstance(inv, dict) else False)
print("next_step = inspect_inventory_payload_shape")
