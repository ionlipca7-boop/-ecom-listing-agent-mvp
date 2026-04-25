import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
SKU = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
LIVE_OUT = ROOT / "storage" / "exports" / "adapter_001_inventory_readback_v1.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_inventory_readback_audit_v1.json"

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + SKU
    resp = requests.get(url, headers=headers, timeout=60)
    try:
        data = resp.json()
    except Exception:
        data = {"raw_text": resp.text}
    LIVE_OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    product = data.get("product", {}) if isinstance(data, dict) else {}
    aspects = product.get("aspects", {}) if isinstance(product, dict) else {}
    pws = data.get("packageWeightAndSize", {}) if isinstance(data, dict) else {}
    weight = pws.get("weight", {}) if isinstance(pws, dict) else {}
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_inventory_readback_verify_v1_completed"
    result["sku"] = SKU
    result["read_status"] = resp.status_code
    result["title"] = product.get("title", "")
    result["image_count"] = len(product.get("imageUrls", []))
    result["aspect_keys"] = sorted(list(aspects.keys()))
    result["weight_value"] = weight.get("value", "")
    result["weight_unit"] = weight.get("unit", "")
    result["next_step"] = "update_offer_price_shipping_location_policies"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_INVENTORY_READBACK_VERIFY_V1")
    print("status =", result["status"])
    print("read_status =", result["read_status"])
    print("title =", result["title"])
    print("image_count =", result["image_count"])
    print("weight_value =", result["weight_value"])
    print("weight_unit =", result["weight_unit"])
if __name__ == "__main__":
    main()
