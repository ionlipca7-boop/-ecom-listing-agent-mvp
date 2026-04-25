import json
from pathlib import Path
import requests
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
SECRET_DIR = BASE_DIR / "storage" / "secrets"
def read_text(path):
    return path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
def main():
    sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
    token_path = SECRET_DIR / "ebay_access_token.txt"
    if not token_path.exists():
        raise FileNotFoundError("Missing file: " + str(token_path))
    token = read_text(token_path)
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Language": "de-DE"}
    response = requests.get(url, headers=headers, timeout=60)
    data = response.json() if response.text.strip() else {}
    out_path = EXPORT_DIR / "adapter_001_live_inventory_item_v2.json"
    audit_path = EXPORT_DIR / "adapter_001_live_inventory_item_audit_v2.json"
    if response.status_code == 200:
        out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {
        "status": "OK" if response.status_code == 200 else "ERROR",
        "decision": "adapter_001_live_inventory_item_v2_fetched" if response.status_code == 200 else "adapter_001_live_inventory_item_v2_fetch_failed",
        "http_status": response.status_code,
        "sku": sku,
        "has_title": bool(data.get("product", {}).get("title")),
        "has_description": bool(data.get("product", {}).get("description")),
        "image_urls_count": len(data.get("product", {}).get("imageUrls", [])),
        "aspects_count": len(data.get("product", {}).get("aspects", {}))
    }
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_LIVE_ITEM_V2_FETCH_DONE")
    print("http_status =", response.status_code)
    print("audit_file =", str(audit_path))
if __name__ == "__main__":
    main()
