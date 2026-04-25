import json
from pathlib import Path

import requests

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
SECRETS = ROOT / "storage" / "secrets"
EXPORTS = ROOT / "storage" / "exports"

input_path = EXPORTS / "first_real_multi_listing_run_payload_v4.json"
output_path = EXPORTS / "first_real_multi_listing_live_run_v1_result.json"
token_path = SECRETS / "ebay_access_token.txt"

data = json.loads(input_path.read_text(encoding="utf-8"))
access_token = token_path.read_text(encoding="utf-8").strip()

inventory_payload = data.get("inventory_payload", {})
offer_payload = data.get("offer_payload", {})

sku = inventory_payload.get("sku") or offer_payload.get("sku")
marketplace_id = offer_payload.get("marketplaceId", "EBAY_DE")

headers_json = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json",
    "Content-Language": "de-DE",
}

result = {
    "status": "ERROR",
    "decision": "first_real_multi_listing_live_run_v1_executed",
    "runtime_ready_for_live": data.get("runtime_ready_for_live"),
    "blocking_fields": data.get("blocking_fields"),
    "sku": sku,
    "marketplace_id": marketplace_id,
}

if not sku:
    result["error"] = "missing_sku_in_inventory_payload_or_offer_payload"
else:
    inventory_url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    inventory_response = requests.put(
        inventory_url,
        headers=headers_json,
        json=inventory_payload,
        timeout=90,
    )

    try:
        inventory_json = inventory_response.json()
    except Exception:
        inventory_json = {"raw_text": inventory_response.text}

    result["inventory_http_status"] = inventory_response.status_code
    result["inventory_response"] = inventory_json

    if inventory_response.status_code in (200, 204):
        create_offer_url = "https://api.ebay.com/sell/inventory/v1/offer"
        offer_response = requests.post(
            create_offer_url,
            headers=headers_json,
            json=offer_payload,
            timeout=90,
        )

        try:
            offer_json = offer_response.json()
        except Exception:
            offer_json = {"raw_text": offer_response.text}

        result["offer_create_http_status"] = offer_response.status_code
        result["offer_create_response"] = offer_json

        offer_id = None
        if isinstance(offer_json, dict):
            offer_id = offer_json.get("offerId")

        result["offer_id"] = offer_id

        if offer_response.status_code in (200, 201) and offer_id:
            publish_url = f"https://api.ebay.com/sell/inventory/v1/offer/{offer_id}/publish"
            publish_response = requests.post(
                publish_url,
                headers=headers_json,
                timeout=90,
            )

            try:
                publish_json = publish_response.json()
            except Exception:
                publish_json = {"raw_text": publish_response.text}

            result["publish_http_status"] = publish_response.status_code
            result["publish_response"] = publish_json

            listing_id = None
            if isinstance(publish_json, dict):
                listing_id = publish_json.get("listingId")

            result["listing_id"] = listing_id

            if publish_response.status_code in (200, 201):
                result["status"] = "OK"
                result["published"] = True
                result["next_step"] = "read_live_offer_and_archive_result"
            else:
                result["published"] = False
                result["next_step"] = "inspect_publish_error"
        else:
            result["published"] = False
            result["next_step"] = "inspect_offer_create_error"
    else:
        result["published"] = False
        result["next_step"] = "inspect_inventory_error"

output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("FIRST_REAL_MULTI_LISTING_LIVE_RUN_V1_FINAL_AUDIT")
print("status =", result.get("status"))
print("decision =", result.get("decision"))
print("runtime_ready_for_live =", result.get("runtime_ready_for_live"))
print("inventory_http_status =", result.get("inventory_http_status"))
print("offer_create_http_status =", result.get("offer_create_http_status"))
print("publish_http_status =", result.get("publish_http_status"))
print("offer_id =", result.get("offer_id"))
print("listing_id =", result.get("listing_id"))
print("published =", result.get("published"))
print("next_step =", result.get("next_step"))