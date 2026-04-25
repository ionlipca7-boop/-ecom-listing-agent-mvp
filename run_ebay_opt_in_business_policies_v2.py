import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
API_URL = "https://api.ebay.com/sell/account/v1/program/opt_in"

def main() -> None:
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
    payload = json.dumps({"programType": "SELLING_POLICY_MANAGEMENT"}).encode("utf-8")

    request = urllib.request.Request(API_URL, data=payload, headers={"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8", errors="replace")
            status_code = response.getcode()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        audit = {"status": "FAILED", "http_status": e.code, "body": body}
        (EXPORTS_DIR / "ebay_opt_in_business_policies_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("OPT_IN_FAILED")
        print("http_status =", e.code)
        print(body)
        raise SystemExit(1)

    parsed = {}
    if body.strip():
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw_body": body}

    audit = {"status": "OK", "http_status": status_code, "body": parsed}
    (EXPORTS_DIR / "ebay_opt_in_business_policies_audit_v2.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print("OPT_IN_OK")
    print("http_status =", status_code)
    if parsed:
        print("top_keys =", list(parsed.keys())[:10])

if __name__ == "__main__":
    main()
