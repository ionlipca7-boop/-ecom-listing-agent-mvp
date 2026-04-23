import json
from pathlib import Path

EXPORTS_DIR = Path("storage") / "exports"
PUBLISH_FILE = EXPORTS_DIR / "ebay_publish_offer_audit_v6.json"
OFFER_FILE = EXPORTS_DIR / "ebay_get_offer_audit_v3.json"
OUTPUT_FILE = EXPORTS_DIR / "ebay_publish_success_summary_v1.json"

def main():
    publish_data = json.loads(PUBLISH_FILE.read_text(encoding="utf-8"))
    offer_data = json.loads(OFFER_FILE.read_text(encoding="utf-8"))
    offer = offer_data.get("response_json") or {}
    summary = {
        "status": "LIVE_PUBLISH_CONFIRMED",
        "offerId": publish_data.get("offerId"),
        "listingId": publish_data.get("listingId"),
        "marketplaceId": offer.get("marketplaceId"),
        "sku": offer.get("sku"),
        "format": offer.get("format"),
        "categoryId": offer.get("categoryId"),
        "availableQuantity": offer.get("availableQuantity"),
        "merchantLocationKey": offer.get("merchantLocationKey"),
        "listingPolicies": {
            "fulfillmentPolicyId": offer.get("listingPolicies", {}).get("fulfillmentPolicyId"),
            "paymentPolicyId": offer.get("listingPolicies", {}).get("paymentPolicyId"),
            "returnPolicyId": offer.get("listingPolicies", {}).get("returnPolicyId"),
        }
    }
    OUTPUT_FILE.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CAPTURE_PUBLISH_SUCCESS_V1_DONE")
    print("listingId =", summary.get("listingId"))
    print("sku =", summary.get("sku"))

if __name__ == "__main__":
    main()
