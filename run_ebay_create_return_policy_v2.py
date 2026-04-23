import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
API_URL = "https://api.ebay.com/sell/account/v1/return_policy"

def main() -> None:
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()

    payload_obj = {
        "name": "ECOM_DE_RETURN_STD_V1",
        "description": "Standard DE return policy created by ECOM Listing Agent MVP",
        "marketplaceId": "EBAY_DE",
        "categoryTypes": [{"name": "ALL_EXCLUDING_MOTORS_VEHICLES"}],
        "returnsAccepted": True,
        "returnPeriod": {"value": 30, "unit": "DAY"},
        "returnMethod": "REPLACEMENT",
        "returnShippingCostPayer": "BUYER"
    }

    payload = json.dumps(payload_obj).encode("utf-8")
    request = urllib.request.Request(API_URL, data=payload, headers={"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8", errors="replace")
            status_code = response.getcode()
            location = response.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        audit = {"status": "FAILED", "http_status": e.code, "body": body}
        (EXPORTS_DIR / "ebay_create_return_policy_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CREATE_RETURN_POLICY_FAILED")
        print("http_status =", e.code)
        print(body)
        raise SystemExit(1)

    data = json.loads(body) if body.strip() else {}
    (EXPORTS_DIR / "ebay_create_return_policy_v2.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {"status": "OK", "http_status": status_code, "location": location, "top_keys": list(data.keys())[:10]}
    (EXPORTS_DIR / "ebay_create_return_policy_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CREATE_RETURN_POLICY_OK")
    print("http_status =", status_code)
    print("location =", location)
    print("top_keys =", list(data.keys())[:10])

if __name__ == "__main__":
    main()
