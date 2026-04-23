import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
TOKEN_PATH = BASE_DIR / "storage" / "secrets" / "ebay_access_token.txt"
EXPORT_PATH = BASE_DIR / "storage" / "exports" / "ebay_policies_v1.json"

def fetch(session, url):
    response = session.get(url, timeout=60)
    try:
        data = response.json()
    except Exception:
        data = {"raw_text": response.text[:1000]}
    return response.status_code, data

def simplify(items, id_key, name_key):
    out = []
    for item in items:
        out.append({
            "id": item.get(id_key),
            "name": item.get(name_key),
            "marketplaceId": item.get("marketplaceId"),
            "categoryTypes": item.get("categoryTypes", [])
        })
    return out

def main():
    token = TOKEN_PATH.read_text(encoding="utf-8").strip()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_DE"
    })

    base = "https://api.ebay.com/sell/account/v1"
    f_status, f_data = fetch(session, base + "/fulfillment_policy?marketplace_id=EBAY_DE")
    p_status, p_data = fetch(session, base + "/payment_policy?marketplace_id=EBAY_DE")
    r_status, r_data = fetch(session, base + "/return_policy?marketplace_id=EBAY_DE")

    fulfillment_items = simplify(f_data.get("fulfillmentPolicies", []), "fulfillmentPolicyId", "name")
    payment_items = simplify(p_data.get("paymentPolicies", []), "paymentPolicyId", "name")
    return_items = simplify(r_data.get("returnPolicies", []), "returnPolicyId", "name")

    result = {
        "status": "OK" if f_status == 200 and p_status == 200 and r_status == 200 else "PARTIAL_OR_FAILED",
        "decision": "policies_fetched",
        "marketplace_id": "EBAY_DE",
        "http_statuses": {
            "fulfillment": f_status,
            "payment": p_status,
            "return": r_status
        },
        "counts": {
            "fulfillment": len(fulfillment_items),
            "payment": len(payment_items),
            "return": len(return_items)
        },
        "fulfillment_policies": fulfillment_items,
        "payment_policies": payment_items,
        "return_policies": return_items,
        "raw_errors": {
            "fulfillment": f_data if f_status != 200 else {},
            "payment": p_data if p_status != 200 else {},
            "return": r_data if r_status != 200 else {}
        }
    }

    EXPORT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("FETCH_EBAY_POLICIES_V1")
    print("fulfillment_http =", f_status)
    print("payment_http =", p_status)
    print("return_http =", r_status)
    print("fulfillment_count =", len(fulfillment_items))
    print("payment_count =", len(payment_items))
    print("return_count =", len(return_items))

if __name__ == "__main__":
    main()
