import json
import urllib.request
import urllib.error
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def read_secret(name):
    return (SECRETS_DIR / name).read_text(encoding="utf-8-sig").strip()

def utc_now():
    return datetime.now(UTC).strftime("%%Y%%m%%d_%%H%%M%%S")

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_secret("ebay_access_token.txt")

    policy_name = "ECOM_DE_PAYMENT_STD_V2_" + utc_now()
    payload = {
        "name": policy_name,
        "description": "ECOM OS DE payment policy",
        "marketplaceId": "EBAY_DE",
        "categoryTypes": [{"name": "ALL_EXCLUDING_MOTORS_VEHICLES"}],
        "immediatePay": False
    }

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.ebay.com/sell/account/v1/payment_policy",
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Content-Language": "de-DE"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.getcode()
            location = resp.headers.get("Location")
            raw = resp.read().decode("utf-8")
        data = json.loads(raw) if raw else {}
        audit = {
            "status": "OK",
            "http_status": status_code,
            "location": location,
            "paymentPolicyId": data.get("paymentPolicyId"),
            "name": data.get("name"),
            "body": data
        }
        (EXPORTS_DIR / "ebay_create_payment_policy_v2.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        (EXPORTS_DIR / "ebay_create_payment_policy_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CREATE_PAYMENT_POLICY_OK")
        print("http_status =", status_code)
        print("location =", location)
        print("paymentPolicyId =", data.get("paymentPolicyId"))
        print("name =", data.get("name"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        audit = {
            "status": "FAILED",
            "http_status": e.code,
            "body": raw,
            "request_payload": payload
        }
        (EXPORTS_DIR / "ebay_create_payment_policy_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("CREATE_PAYMENT_POLICY_FAILED")
        print("http_status =", e.code)
        print(raw)

if __name__ == "__main__":
    main()
