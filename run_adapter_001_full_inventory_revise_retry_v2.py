import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
SRC_PAYLOAD = ROOT / "storage" / "exports" / "adapter_001_full_inventory_revise_payload_v1.json"
PAYLOAD_OUT = ROOT / "storage" / "exports" / "adapter_001_full_inventory_revise_payload_v2.json"
RESPONSE_OUT = ROOT / "storage" / "exports" / "adapter_001_full_inventory_revise_response_v2.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_full_inventory_revise_audit_v2.json"
DEFAULT_WEIGHT = "0.05"
DEFAULT_UNIT = "KILOGRAM"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    payload = load_json(SRC_PAYLOAD)
    pws = payload.get("packageWeightAndSize", {})
    if not isinstance(pws, dict):
        pws = {}
    weight = pws.get("weight", {})
    if not isinstance(weight, dict):
        weight = {}
    old_value = weight.get("value", "")
    old_unit = weight.get("unit", "")
    weight["value"] = DEFAULT_WEIGHT
    if not old_unit:
        weight["unit"] = DEFAULT_UNIT
    pws["weight"] = weight
    payload["packageWeightAndSize"] = pws
    sku = payload.get("sku", "")
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    PAYLOAD_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    resp = requests.put(url, headers=headers, json=payload, timeout=60)
    try:
        resp_data = resp.json()
    except Exception:
        resp_data = {"raw_text": resp.text}
    RESPONSE_OUT.write_text(json.dumps(resp_data, indent=2, ensure_ascii=False), encoding="utf-8")
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_full_inventory_revise_retry_v2_completed"
    result["sku"] = sku
    result["revise_status"] = resp.status_code
    result["old_weight_value"] = old_value
    result["old_weight_unit"] = old_unit
    result["new_weight_value"] = weight.get("value", "")
    result["new_weight_unit"] = weight.get("unit", "")
    result["title"] = payload.get("product", {}).get("title", "")
    result["image_count"] = len(payload.get("product", {}).get("imageUrls", []))
    result["next_step"] = "read_back_inventory_if_revise_ok_else_read_exact_response_v2"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_FULL_INVENTORY_REVISE_RETRY_V2")
    print("status =", result["status"])
    print("sku =", result["sku"])
    print("revise_status =", result["revise_status"])
    print("old_weight_value =", result["old_weight_value"])
    print("new_weight_value =", result["new_weight_value"])
    print("new_weight_unit =", result["new_weight_unit"])
if __name__ == "__main__":
    main()
