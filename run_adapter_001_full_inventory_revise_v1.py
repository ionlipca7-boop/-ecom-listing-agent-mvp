import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
LIVE_INV_PATH = ROOT / "storage" / "exports" / "adapter_001_live_inventory_bridge_read_v1.json"
ENRICHED_PATH = ROOT / "storage" / "exports" / "adapter_001_enriched_revise_payload_v3.json"
PAYLOAD_OUT = ROOT / "storage" / "exports" / "adapter_001_full_inventory_revise_payload_v1.json"
RESPONSE_OUT = ROOT / "storage" / "exports" / "adapter_001_full_inventory_revise_response_v1.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_full_inventory_revise_audit_v1.json"
DEFAULT_TITLE = "USB-C auf USB-A OTG Adapter USB 3.0 Typ-C Datenadapter"
DEFAULT_DESC = "USB-C auf USB-A OTG Adapter fuer schnelle Datenuebertragung und einfache Verbindung von USB-A Geraeten an USB-C Anschluesse. Ideal fuer Smartphone, Tablet, Laptop und Alltag. Kompakt, leicht und praktisch fuer unterwegs."

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def pick_images(live_data, enriched_data):
    imgs = []
    live_product = live_data.get("product", {}) if isinstance(live_data, dict) else {}
    enriched_product = enriched_data.get("product", {}) if isinstance(enriched_data, dict) else {}
    a = enriched_product.get("imageUrls", []) if isinstance(enriched_product, dict) else []
    b = live_product.get("imageUrls", []) if isinstance(live_product, dict) else []
    for group in [a, b]:
        for x in group:
            if x and x not in imgs:
                imgs.append(x)
    return imgs

def merge_aspects(live_data, enriched_data):
    aspects = {}
    live_product = live_data.get("product", {}) if isinstance(live_data, dict) else {}
    enriched_product = enriched_data.get("product", {}) if isinstance(enriched_data, dict) else {}
    live_aspects = live_product.get("aspects", {}) if isinstance(live_product, dict) else {}
    enriched_aspects = enriched_product.get("aspects", {}) if isinstance(enriched_product, dict) else {}
    if isinstance(live_aspects, dict):
        aspects.update(live_aspects)
    if isinstance(enriched_aspects, dict):
        aspects.update(enriched_aspects)
    aspects["Produktart"] = ["OTG Adapter"]
    aspects["Anschluss A"] = ["USB-C"]
    aspects["Anschluss B"] = ["USB-A"]
    aspects["Version"] = ["USB 3.0"]
    return aspects

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    live_data = load_json(LIVE_INV_PATH)
    enriched_data = load_json(ENRICHED_PATH) if ENRICHED_PATH.exists() else {}
    payload = dict(live_data)
    product = dict(payload.get("product", {}))
    enriched_product = enriched_data.get("product", {}) if isinstance(enriched_data, dict) else {}
    title = enriched_product.get("title", "") if isinstance(enriched_product, dict) else ""
    description = enriched_product.get("description", "") if isinstance(enriched_product, dict) else ""
    if not title:
        title = DEFAULT_TITLE
    if not description:
        description = DEFAULT_DESC
    product["title"] = title
    product["description"] = description
    images = pick_images(live_data, enriched_data)
    if images:
        product["imageUrls"] = images
    product["aspects"] = merge_aspects(live_data, enriched_data)
    payload["product"] = product
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
    result["decision"] = "adapter_001_full_inventory_revise_v1_completed"
    result["sku"] = sku
    result["revise_status"] = resp.status_code
    result["title"] = product.get("title", "")
    result["image_count"] = len(product.get("imageUrls", []))
    result["aspect_keys"] = sorted(list(product.get("aspects", {}).keys()))[:20]
    result["payload_out"] = str(PAYLOAD_OUT.relative_to(ROOT))
    result["response_out"] = str(RESPONSE_OUT.relative_to(ROOT))
    result["next_step"] = "read_back_inventory_and_then_update_offer_price_shipping_location"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_FULL_INVENTORY_REVISE_V1")
    print("status =", result["status"])
    print("sku =", result["sku"])
    print("revise_status =", result["revise_status"])
    print("title =", result["title"])
    print("image_count =", result["image_count"])
if __name__ == "__main__":
    main()
