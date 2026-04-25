import json
import requests
from pathlib import Path

def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return json.loads(path.read_text(encoding="utf-8-sig"))

def read_text(path):
    return path.read_text(encoding="utf-8").strip()

base = Path(".")
payload_path = base / "storage" / "exports" / "safe_full_offer_payload_v2.json"
out_path = base / "storage" / "exports" / "real_full_offer_revise_v1_result.json"
token_path = base / "storage" / "secrets" / "ebay_access_token.txt"

data = load_json(payload_path)
payload = data["payload"]
offer_id = data["offer_id"]
token = read_text(token_path)

url = "https://api.ebay.com/sell/inventory/v1/offer/" + str(offer_id)
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE",
    "Accept": "application/json"
}

response = requests.put(url, headers=headers, json=payload, timeout=60)

try:
    response_json = response.json()
except Exception:
    response_json = None

result = {
    "status": "OK" if response.status_code in [200, 204] else "FAILED",
    "decision": "real_full_offer_revise_v1_executed",
    "offer_id": offer_id,
    "sku": data["sku"],
    "http_status": response.status_code,
    "ok": response.ok,
    "sent_image_urls_count": len(payload.get("imageUrls", [])),
    "sent_has_listingPolicies": bool(payload.get("listingPolicies")),
    "sent_has_merchantLocationKey": bool(payload.get("merchantLocationKey")),
    "sent_has_listingDescription": bool(payload.get("listingDescription")),
    "sent_has_availableQuantity": payload.get("availableQuantity") not in [None, ""],
    "response_text": response.text[:4000],
    "response_json": response_json,
    "next_step": "read_live_offer_after_full_revise_v1" if response.status_code in [200, 204] else "inspect_exact_api_error_v1"
}

out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("REAL_FULL_OFFER_REVISE_V1_DONE")
print("http_status =", result["http_status"])
print("offer_id =", result["offer_id"])
print("sent_image_urls_count =", result["sent_image_urls_count"])
print("next_step =", result["next_step"])
