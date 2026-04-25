import json
from pathlib import Path
ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
EXPORTS = ROOT / "storage" / "exports"
current_path = EXPORTS / "first_real_multi_listing_run_payload_v4.json"
inv_src_path = EXPORTS / "adapter_001_content_upgrade_inventory_payload_v2.json"
offer_src_path = EXPORTS / "adapter_001_content_upgrade_offer_payload_v2.json"
out_path = EXPORTS / "first_real_multi_listing_run_payload_v5.json"
current = json.loads(current_path.read_text(encoding="utf-8"))
inv_src = json.loads(inv_src_path.read_text(encoding="utf-8"))
offer_src = json.loads(offer_src_path.read_text(encoding="utf-8"))
sku = current.get("inventory_payload", {}).get("sku") or current.get("offer_payload", {}).get("sku")
title = current.get("inventory_payload", {}).get("title")
category_id = current.get("inventory_payload", {}).get("category_id")
merchant_location_key = current.get("inventory_payload", {}).get("merchant_location_key")
price = current.get("offer_payload", {}).get("price")
f_id = current.get("applied_real_policy_ids", {}).get("fulfillmentPolicyId")
p_id = current.get("applied_real_policy_ids", {}).get("paymentPolicyId")
r_id = current.get("applied_real_policy_ids", {}).get("returnPolicyId")
inventory_payload = dict(inv_src)
offer_payload = dict(offer_src)
inventory_payload["sku"] = sku
if title and "product" in inventory_payload and isinstance(inventory_payload["product"], dict):
    inventory_payload["product"]["title"] = title
if "availability" not in inventory_payload:
    inventory_payload["availability"] = {}
if "shipToLocationAvailability" not in inventory_payload["availability"]:
    inventory_payload["availability"]["shipToLocationAvailability"] = {}
if "quantity" not in inventory_payload["availability"]["shipToLocationAvailability"]:
    inventory_payload["availability"]["shipToLocationAvailability"]["quantity"] = 10
offer_payload["sku"] = sku
if category_id:
    offer_payload["categoryId"] = str(category_id)
if merchant_location_key:
    offer_payload["merchantLocationKey"] = merchant_location_key
if price is not None:
    if "pricingSummary" not in offer_payload:
        offer_payload["pricingSummary"] = {}
    offer_payload["pricingSummary"]["price"] = {"value": str(price), "currency": "EUR"}
if "listingPolicies" not in offer_payload:
    offer_payload["listingPolicies"] = {}
offer_payload["listingPolicies"]["fulfillmentPolicyId"] = f_id
offer_payload["listingPolicies"]["paymentPolicyId"] = p_id
offer_payload["listingPolicies"]["returnPolicyId"] = r_id
if "availableQuantity" not in offer_payload:
    offer_payload["availableQuantity"] = 10
result = dict(current)
result["status"] = "OK"
result["decision"] = "real_multi_listing_run_payload_v5_built_from_archived_real_sources"
result["inventory_payload"] = inventory_payload
result["offer_payload"] = offer_payload
result["runtime_ready_for_live"] = True
result["blocking_fields"] = []
result["payload_source_inventory"] = inv_src_path.name
result["payload_source_offer"] = offer_src_path.name
result["next_step"] = "execute_first_real_multi_listing_live_run_v2"
out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("BUILD_REAL_MULTI_LISTING_PAYLOAD_V5_FINAL_AUDIT")
print("status = OK")
print("sku =", sku)
print("inventory_source =", inv_src_path.name)
print("offer_source =", offer_src_path.name)
print("inventory_keys =", list(inventory_payload.keys()))
print("offer_keys =", list(offer_payload.keys()))
print("price_value =", offer_payload.get("pricingSummary", {}).get("price", {}).get("value"))
print("fulfillmentPolicyId =", offer_payload.get("listingPolicies", {}).get("fulfillmentPolicyId"))
print("paymentPolicyId =", offer_payload.get("listingPolicies", {}).get("paymentPolicyId"))
print("returnPolicyId =", offer_payload.get("listingPolicies", {}).get("returnPolicyId"))
print("next_step =", result.get("next_step"))
