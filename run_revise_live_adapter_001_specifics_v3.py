import json
from pathlib import Path
import requests
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
SECRET_DIR = BASE_DIR / "storage" / "secrets"
def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))
def read_text(path):
    return path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
def main():
    payload_path = EXPORT_DIR / "adapter_001_enriched_revise_payload_v2.json"
    token_path = SECRET_DIR / "ebay_access_token.txt"
    if not payload_path.exists():
        raise FileNotFoundError("Missing file: " + str(payload_path))
    if not token_path.exists():
        raise FileNotFoundError("Missing file: " + str(token_path))
    d = read_json(payload_path)
    token = read_text(token_path)
    payload = d["payload"]
    sku = payload["sku"]
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + sku
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json", "Content-Language": "de-DE", "Accept": "application/json"}
    response = requests.put(url, headers=headers, json=payload, timeout=60)
    raw_text = response.text
    try:
        response_json = response.json() if raw_text.strip() else {}
    except Exception:
        response_json = {"raw_text": raw_text}
    audit = {
        "status": "OK" if response.status_code in (200, 204) else "ERROR",
        "decision": "adapter_001_live_revise_v3_ok" if response.status_code in (200, 204) else "adapter_001_live_revise_v3_failed",
        "http_status": response.status_code,
        "product_key": "adapter_001",
        "sku": sku,
        "offerId": d.get("offerId"),
        "listingId": d.get("listingId"),
        "image_urls_count": len(payload.get("product", {}).get("imageUrls", [])),
        "aspects_count": len(payload.get("product", {}).get("aspects", {})),
        "response_body": response_json
    }
    out_path = EXPORT_DIR / "adapter_001_live_revise_audit_v3.json"
    out_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    if response.status_code in (200, 204):
        print("ADAPTER_001_LIVE_REVISE_V3_OK")
    else:
        print("ADAPTER_001_LIVE_REVISE_V3_FAILED")
    print("http_status =", response.status_code)
    print("sku =", sku)
    print("image_urls_count =", len(payload.get("product", {}).get("imageUrls", [])))
    print("aspects_count =", len(payload.get("product", {}).get("aspects", {})))
    print("audit_file =", str(out_path))
if __name__ == "__main__":
    main()
