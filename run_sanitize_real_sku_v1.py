import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "real_offer_request_payload_v3.json"
OUTPUT_PATH = EXPORTS_DIR / "real_offer_request_payload_v4.json"

def make_safe_sku(value):
    cleaned = re.sub(r"[^A-Za-z0-9]", "", value or "")
    if not cleaned:
        cleaned = "USBCLadekabel2m60W"
    return cleaned[:50]

def main():
    data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    payload = data.get("payload", {})
    old_sku = payload.get("sku", "")
    new_sku = make_safe_sku(old_sku)
    payload["sku"] = new_sku
    result = {
        "status": "OK",
        "decision": "sku_sanitized_for_real_api",
        "old_sku": old_sku,
        "new_sku": new_sku,
        "new_sku_length": len(new_sku),
        "payload": payload
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SANITIZE_REAL_SKU_V1")
    print("old_sku =", old_sku)
    print("new_sku =", new_sku)
    print("new_sku_length =", len(new_sku))

if __name__ == "__main__":
    main()
