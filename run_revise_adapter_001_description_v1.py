import json
from datetime import UTC, datetime
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
INPUT_FILE = BASE_DIR / "storage" / "exports" / "new_product_adapter_001.json"
HTML_FILE = BASE_DIR / "storage" / "exports" / "adapter_001_html_description_clean_v1.json"
PREV_FILE = BASE_DIR / "storage" / "exports" / "publish_existing_offer_repair_v3.json"
OUT_FILE = BASE_DIR / "storage" / "exports" / "adapter_001_description_revise_v1.json"

IMAGE_URLS = [
    "https://ae01.alicdn.com/kf/S42fabc33d69c4f5592466804c540a072T.jpg",
    "https://ae01.alicdn.com/kf/Sc68f16cdbb0e48ca9f68da607d90f55fO.jpg",
    "https://ae01.alicdn.com/kf/Sceae79ed63dc4d5aab039de4a52879c8r.jpg",
    "https://ae01.alicdn.com/kf/S8893d5727a1446bb860b97548ede5410X.jpg",
    "https://ae01.alicdn.com/kf/S4f8750a0169946e0b4fc1a0f1b23089aB.jpg",
    "https://ae01.alicdn.com/kf/S3a9306f37bbf44d28dcc5d7b5aaa5c7bl.jpg",
    "https://ae01.alicdn.com/kf/Sadcd253f429a49b8a3460fe75febf721R.jpg",
    "https://ae01.alicdn.com/kf/Se63d8168e9664e28b5c0878026e2445an.jpg",
    "https://ae01.alicdn.com/kf/S21d6d1cf19c341c7928d286cd6a6e8957.jpg"
]

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def read_text(path):
    return path.read_text(encoding="utf-8").strip()

def ensure_list(value):
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]

def main():
    product = read_json(INPUT_FILE)
    html_data = read_json(HTML_FILE)
    prev = read_json(PREV_FILE)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")
    sku = prev.get("sku")
    title = product.get("title") or product.get("main_title") or "USB-C OTG Adapter USB 3.0 Typ-C auf USB-A Schnellladen Daten"
    raw_aspects = product.get("aspects") if isinstance(product.get("aspects"), dict) else {}
    aspects = {}
    for k, v in raw_aspects.items():
        key = str(k).strip()
        vals = ensure_list(v)
        if key and vals:
            aspects[key] = vals
    aspects["Produktart"] = ensure_list(aspects.get("Produktart") or product.get("produktart") or "USB-C OTG Adapter")
    aspects["Marke"] = ensure_list(product.get("brand") or "No-Name")
    aspects["Herstellernummer"] = ensure_list(product.get("mpn") or "Nicht zutreffend")
    payload = {
        "availability": {"shipToLocationAvailability": {"quantity": int(product.get("quantity", 10))}},
        "condition": "NEW",
        "product": {
            "title": title,
            "description": html_data.get("html", ""),
            "aspects": aspects,
            "imageUrls": IMAGE_URLS
        }
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Content-Language": "de-DE"}
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    response = requests.put(url, headers=headers, json=payload, timeout=60)
    result = {
        "status": "OK" if response.status_code in (200, 201, 204) else "ERROR",
        "decision": "adapter_001_description_revised" if response.status_code in (200, 201, 204) else "adapter_001_description_revise_failed",
        "updated_at_utc": datetime.now(UTC).isoformat(),
        "sku": sku,
        "http_status": response.status_code,
        "description_length": len(html_data.get("html", "")),
        "payload": payload
    }
    try:
        result["response"] = response.json()
    except Exception:
        result["response_text"] = response.text
    OUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("ADAPTER_001_DESCRIPTION_REVISE_DONE")
    print("status =", result["status"])
    print("decision =", result["decision"])
    print("sku =", result["sku"])
    print("http_status =", result["http_status"])
    print("description_length =", result["description_length"])

if __name__ == "__main__":
    main()
