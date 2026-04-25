import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
OFFER_ID = "153365657011"
SKU_FALLBACK = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
OFFER_OUT = ROOT / "storage" / "exports" / "adapter_001_live_offer_bridge_read_v1.json"
INV_OUT = ROOT / "storage" / "exports" / "adapter_001_live_inventory_bridge_read_v1.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "live_offer_inventory_bridge_read_audit_v1.json"

def read_token():
    return TOKEN_PATH.read_text(encoding="utf-8").strip()

def main():
    token = read_token()
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    offer_url = "https://api.ebay.com/sell/inventory/v1/offer/" + OFFER_ID
    offer_resp = requests.get(offer_url, headers=headers, timeout=60)
    offer_text = offer_resp.text
    try:
        offer_data = offer_resp.json()
    except Exception:
        offer_data = {"raw_text": offer_text}
    OFFER_OUT.write_text(json.dumps(offer_data, indent=2, ensure_ascii=False), encoding="utf-8")
    live_sku = offer_data.get("sku", "") if isinstance(offer_data, dict) else ""
    if not live_sku:
        live_sku = SKU_FALLBACK
    inv_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + live_sku
    inv_resp = requests.get(inv_url, headers=headers, timeout=60)
    inv_text = inv_resp.text
    try:
        inv_data = inv_resp.json()
    except Exception:
        inv_data = {"raw_text": inv_text}
    INV_OUT.write_text(json.dumps(inv_data, indent=2, ensure_ascii=False), encoding="utf-8")
    result = {}
    result["status"] = "OK"
    result["decision"] = "live_offer_inventory_bridge_read_v1_completed"
    result["offer_id"] = OFFER_ID
    result["offer_get_status"] = offer_resp.status_code
    result["live_sku"] = live_sku
    result["inventory_get_status"] = inv_resp.status_code
    result["offer_out"] = str(OFFER_OUT.relative_to(ROOT))
    result["inventory_out"] = str(INV_OUT.relative_to(ROOT))
    result["next_step"] = "build_full_live_revise_payload_from_offer_and_inventory_if_inventory_exists"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("LIVE_OFFER_INVENTORY_BRIDGE_READ_V1")
    print("status =", result["status"])
    print("offer_id =", result["offer_id"])
    print("offer_get_status =", result["offer_get_status"])
    print("live_sku =", result["live_sku"])
    print("inventory_get_status =", result["inventory_get_status"])
if __name__ == "__main__":
    main()
