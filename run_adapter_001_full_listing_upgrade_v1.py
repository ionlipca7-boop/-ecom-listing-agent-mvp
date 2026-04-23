import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
SKU = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
OFFER_ID = "153365657011"
INV_PAYLOAD_OUT = ROOT / "storage" / "exports" / "adapter_001_full_listing_upgrade_inventory_payload_v1.json"
INV_RESPONSE_OUT = ROOT / "storage" / "exports" / "adapter_001_full_listing_upgrade_inventory_response_v1.json"
OFFER_PAYLOAD_OUT = ROOT / "storage" / "exports" / "adapter_001_full_listing_upgrade_offer_payload_v1.json"
OFFER_RESPONSE_OUT = ROOT / "storage" / "exports" / "adapter_001_full_listing_upgrade_offer_response_v1.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_full_listing_upgrade_audit_v1.json"
TITLE = "USB-C auf USB-A OTG Adapter USB 3.0 Datenadapter Handy Tablet"
DESC = "USB-C auf USB-A OTG Adapter fuer schnelle Datenuebertragung und die einfache Verbindung von USB-A Geraeten mit USB-C Anschluessen. Ideal fuer Smartphone, Tablet, Laptop, USB-Stick, Tastatur, Maus und andere kompatible Geraete. Kompakt, leicht und praktisch fuer Alltag, Reisen, Auto und Buero."
HTML = "<h2>USB-C auf USB-A OTG Adapter USB 3.0</h2><p><b>Kompakt, schnell und alltagstauglich.</b></p><p>Dieser praktische OTG Adapter verbindet USB-A Geraete mit einem USB-C Anschluss und eignet sich ideal fuer Smartphone, Tablet, Laptop und viele weitere kompatible Geraete.</p><ul><li>USB-C auf USB-A Adapter</li><li>USB 3.0 fuer schnelle Datenuebertragung</li><li>Kompaktes Format fuer unterwegs</li><li>Passend fuer viele moderne Geraete mit USB-C</li><li>Ideal fuer USB-Stick, Maus, Tastatur und mehr</li></ul><p><b>Vorteile:</b></p><ul><li>Schnelle und stabile Verbindung</li><li>Einfache Nutzung ohne komplizierte Einrichtung</li><li>Leicht, platzsparend und reisetauglich</li></ul><p><b>Hinweis:</b> Bitte vor dem Kauf die Kompatibilitaet Ihres Geraets pruefen.</p><p><b>Schneller Versand aus Deutschland.</b></p>"

def get_json(url, headers):
    resp = requests.get(url, headers=headers, timeout=60)
    try:
        data = resp.json()
    except Exception:
        data = {"raw_text": resp.text}
    return resp, data

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    inv_url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + SKU
    offer_url = "https://api.ebay.com/sell/inventory/v1/offer/" + OFFER_ID
    inv_get_resp, inv_live = get_json(inv_url, headers)
    offer_get_resp, offer_live = get_json(offer_url, headers)
    inv_payload = dict(inv_live)
    product = dict(inv_payload.get("product", {}))
    product["title"] = TITLE
    product["description"] = DESC
    live_images = product.get("imageUrls", [])
    if not isinstance(live_images, list):
        live_images = []
    product["imageUrls"] = live_images
    aspects = product.get("aspects", {})
    if not isinstance(aspects, dict):
        aspects = {}
    aspects["Produktart"] = ["OTG Adapter"]
    aspects["Anschluss A"] = ["USB-C"]
    aspects["Anschluss B"] = ["USB-A"]
    aspects["Version"] = ["USB 3.0"]
    aspects["Farbe"] = ["Schwarz"]
    aspects["Material"] = ["Kunststoff"]
    aspects["Besonderheiten"] = ["Kompakt", "Tragbar", "OTG Funktion"]
    aspects["Kompatibel mit"] = ["Smartphone", "Tablet", "Laptop", "USB-Stick", "Maus", "Tastatur"]
    product["aspects"] = aspects
    inv_payload["product"] = product
    pws = inv_payload.get("packageWeightAndSize", {})
    if not isinstance(pws, dict):
        pws = {}
    weight = pws.get("weight", {})
    if not isinstance(weight, dict):
        weight = {}
    weight["value"] = "0.05"
    weight["unit"] = "KILOGRAM"
    pws["weight"] = weight
    inv_payload["packageWeightAndSize"] = pws
    INV_PAYLOAD_OUT.write_text(json.dumps(inv_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    inv_put_resp = requests.put(inv_url, headers=headers, json=inv_payload, timeout=60)
    try:
        inv_put_data = inv_put_resp.json()
    except Exception:
        inv_put_data = {"raw_text": inv_put_resp.text}
    INV_RESPONSE_OUT.write_text(json.dumps(inv_put_data, indent=2, ensure_ascii=False), encoding="utf-8")
    offer_payload = {}
    offer_payload["sku"] = offer_live.get("sku", SKU)
    offer_payload["marketplaceId"] = offer_live.get("marketplaceId", "EBAY_DE")
    offer_payload["format"] = offer_live.get("format", "FIXED_PRICE")
    offer_payload["availableQuantity"] = offer_live.get("availableQuantity", 12)
    offer_payload["categoryId"] = offer_live.get("categoryId", "44932")
    offer_payload["merchantLocationKey"] = offer_live.get("merchantLocationKey", "ECOM_DE_LOC_1")
    offer_payload["listingPolicies"] = offer_live.get("listingPolicies", {"paymentPolicyId": "257755913024", "returnPolicyId": "257755877024", "fulfillmentPolicyId": "257755855024", "eBayPlusIfEligible": False})
    offer_payload["pricingSummary"] = {"price": {"value": "3.99", "currency": "EUR"}}
    offer_payload["listingDescription"] = HTML
    if "quantityLimitPerBuyer" in offer_live:
        offer_payload["quantityLimitPerBuyer"] = offer_live.get("quantityLimitPerBuyer")
    if "tax" in offer_live:
        offer_payload["tax"] = offer_live.get("tax", {})
    OFFER_PAYLOAD_OUT.write_text(json.dumps(offer_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    offer_put_resp = requests.put(offer_url, headers=headers, json=offer_payload, timeout=60)
    try:
        offer_put_data = offer_put_resp.json()
    except Exception:
        offer_put_data = {"raw_text": offer_put_resp.text}
    OFFER_RESPONSE_OUT.write_text(json.dumps(offer_put_data, indent=2, ensure_ascii=False), encoding="utf-8")
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_full_listing_upgrade_v1_completed"
    result["inventory_get_status"] = inv_get_resp.status_code
    result["inventory_put_status"] = inv_put_resp.status_code
    result["offer_get_status"] = offer_get_resp.status_code
    result["offer_put_status"] = offer_put_resp.status_code
    result["title"] = TITLE
    result["image_count_preserved"] = len(live_images)
    result["price_value"] = "3.99"
    result["merchantLocationKey"] = offer_payload.get("merchantLocationKey", "")
    result["listingPolicies"] = offer_payload.get("listingPolicies", {})
    result["next_step"] = "user_check_live_listing_then_decide_photo_set_upgrade"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_FULL_LISTING_UPGRADE_V1")
    print("status =", result["status"])
    print("inventory_put_status =", result["inventory_put_status"])
    print("offer_put_status =", result["offer_put_status"])
    print("title =", result["title"])
    print("image_count_preserved =", result["image_count_preserved"])
if __name__ == "__main__":
    main()
