import json
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
MARKETPLACE_ID = "EBAY_DE"

URLS = {
    "fulfillment": "https://api.ebay.com/sell/account/v1/fulfillment_policy",
    "payment": "https://api.ebay.com/sell/account/v1/payment_policy",
    "return": "https://api.ebay.com/sell/account/v1/return_policy",
}

def fetch_json(url: str, token: str) -> tuple[int, dict]:
    full_url = url + "?" + urllib.parse.urlencode({"marketplace_id": MARKETPLACE_ID})
    request = urllib.request.Request(full_url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}, method="GET")
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8", errors="replace")
        return response.getcode(), json.loads(body)

def main() -> None:
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
    full_output = {"marketplace_id": MARKETPLACE_ID, "status": "OK", "results": {}}
    audit = {"marketplace_id": MARKETPLACE_ID, "status": "OK"}

    try:
        for name, url in URLS.items():
            status_code, data = fetch_json(url, token)
            full_output["results"][name] = {"http_status": status_code, "data": data}
            if isinstance(data, dict):
                if name == "fulfillment":
                    count = len(data.get("fulfillmentPolicies", []))
                elif name == "payment":
                    count = len(data.get("paymentPolicies", []))
                elif name == "return":
                    count = len(data.get("returnPolicies", []))
            audit[name] = {"http_status": status_code, "count": count}

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        error_audit = {"status": "FAILED", "http_status": e.code, "body": body}
        (EXPORTS_DIR / "ebay_business_policies_readiness_v1.json").write_text(json.dumps(error_audit, ensure_ascii=False, indent=2), encoding="utf-8")
        (EXPORTS_DIR / "ebay_business_policies_readiness_audit_v1.json").write_text(json.dumps(error_audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("BUSINESS_POLICIES_READINESS_FAILED")
        print("http_status =", e.code)
        print(body)
        raise SystemExit(1)

    (EXPORTS_DIR / "ebay_business_policies_readiness_v1.json").write_text(json.dumps(full_output, ensure_ascii=False, indent=2), encoding="utf-8")
    (EXPORTS_DIR / "ebay_business_policies_readiness_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print("BUSINESS_POLICIES_READINESS_OK")
    print("marketplace_id =", MARKETPLACE_ID)
    print("fulfillment_count =", audit["fulfillment"]["count"])
    print("payment_count =", audit["payment"]["count"])
    print("return_count =", audit["return"]["count"])

if __name__ == "__main__":
    main()
