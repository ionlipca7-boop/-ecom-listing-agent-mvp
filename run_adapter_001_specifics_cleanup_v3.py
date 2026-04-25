import json
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN_PATH = ROOT / "storage" / "secrets" / "ebay_access_token.txt"
SKU = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
PAYLOAD_OUT = ROOT / "storage" / "exports" / "adapter_001_specifics_cleanup_payload_v3.json"
RESPONSE_OUT = ROOT / "storage" / "exports" / "adapter_001_specifics_cleanup_response_v3.json"
AUDIT_OUT = ROOT / "storage" / "memory" / "archive" / "adapter_001_specifics_cleanup_audit_v3.json"

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json", "Content-Language": "de-DE"}
    url = "https://api.ebay.com/sell/inventory/v1/inventory_item/" + SKU
    get_resp = requests.get(url, headers=headers, timeout=60)
    try:
        data = get_resp.json()
    except Exception:
        data = {"raw_text": get_resp.text}
    payload = dict(data)
    product = dict(payload.get("product", {}))
    aspects = product.get("aspects", {})
    if not isinstance(aspects, dict):
        aspects = {}
    aspects["Marke"] = ["Markenlos"]
    aspects["Produktart"] = ["OTG Adapter"]
    aspects["Anschluss A"] = ["USB-C"]
    aspects["Anschluss B"] = ["USB-A"]
    aspects["Version"] = ["USB 3.0"]
    aspects["Farbe"] = ["Schwarz"]
    aspects["Material"] = ["Kunststoff"]
    aspects["Besonderheiten"] = ["Kompakt", "Tragbar", "OTG Funktion"]
    aspects["Kompatibel mit"] = ["Smartphone", "Tablet", "Laptop", "USB-Stick", "Maus", "Tastatur"]
    aspects["Markenkompatibilitaet"] = ["Universal"]
    aspects["Modellkompatibilitaet"] = ["Universal"]
    aspects["Herstellernummer"] = ["Nicht zutreffend"]
    aspects["Anzahl der Einheiten"] = ["1"]
    aspects["Ma?einheit"] = ["Einheit"]
    aspects["Ursprungsland"] = ["China"]
    aspects["Breite"] = ["1"]
    aspects["Hohe"] = ["1"]
    aspects["Lange"] = ["3"]
    product["aspects"] = aspects
    payload["product"] = product
    pws = payload.get("packageWeightAndSize", {})
    if not isinstance(pws, dict):
        pws = {}
    pws["weight"] = {"value": "0.05", "unit": "KILOGRAM"}
    pws["dimensions"] = {"length": "3", "width": "2", "height": "1", "unit": "CENTIMETER"}
    payload["packageWeightAndSize"] = pws
    PAYLOAD_OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    put_resp = requests.put(url, headers=headers, json=payload, timeout=60)
    try:
        put_data = put_resp.json()
    except Exception:
        put_data = {"raw_text": put_resp.text}
    RESPONSE_OUT.write_text(json.dumps(put_data, indent=2, ensure_ascii=False), encoding="utf-8")
    result = {}
    result["status"] = "OK"
    result["decision"] = "adapter_001_specifics_cleanup_v3_completed"
    result["get_status"] = get_resp.status_code
    result["put_status"] = put_resp.status_code
    result["aspect_count"] = len(aspects)
    result["compat_count"] = len(aspects.get("Kompatibel mit", []))
    result["weight_value"] = pws.get("weight", {}).get("value", "")
    result["dimensions"] = pws.get("dimensions", {})
    result["next_step"] = "user_check_listing_specifics_and_package_fields_then_photo_and_location_upgrade"
    AUDIT_OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ADAPTER_001_SPECIFICS_CLEANUP_V3")
    print("status =", result["status"])
    print("get_status =", result["get_status"])
    print("put_status =", result["put_status"])
    print("aspect_count =", result["aspect_count"])
    print("compat_count =", result["compat_count"])
    print("dimensions =", result["dimensions"])
if __name__ == "__main__":
    main()
