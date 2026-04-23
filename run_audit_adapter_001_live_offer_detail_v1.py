import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
OFFER_PATH = BASE_DIR / "storage" / "exports" / "adapter_001_live_offer_v2.json"
def main():
    data = json.loads(OFFER_PATH.read_text(encoding="utf-8"))
    price = data.get("pricingSummary", {}).get("price", {})
    policies = data.get("listingPolicies", {})
    print("ADAPTER_001_LIVE_OFFER_DETAIL_AUDIT")
    print("offerId =", data.get("offerId"))
    print("sku =", data.get("sku"))
    print("marketplaceId =", data.get("marketplaceId"))
    print("format =", data.get("format"))
    print("categoryId =", data.get("categoryId"))
    print("merchantLocationKey =", data.get("merchantLocationKey"))
    print("availableQuantity =", data.get("availableQuantity"))
    print("price_value =", price.get("value"))
    print("price_currency =", price.get("currency"))
    print("fulfillmentPolicyId =", policies.get("fulfillmentPolicyId"))
    print("paymentPolicyId =", policies.get("paymentPolicyId"))
    print("returnPolicyId =", policies.get("returnPolicyId"))
if __name__ == "__main__":
    main()
