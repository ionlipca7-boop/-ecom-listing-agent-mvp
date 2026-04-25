import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
API_URL = "https://api.ebay.com/sell/account/v1/program/get_opted_in_programs"

def main() -> None:
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
    request = urllib.request.Request(API_URL, headers={"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}, method="GET")

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8", errors="replace")
            status_code = response.getcode()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        audit = {"status": "FAILED", "http_status": e.code, "body": body}
        (EXPORTS_DIR / "ebay_get_opted_in_programs_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("GET_OPTED_IN_PROGRAMS_FAILED")
        print("http_status =", e.code)
        print(body)
        raise SystemExit(1)

    data = json.loads(body)
    (EXPORTS_DIR / "ebay_get_opted_in_programs_v1.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    audit = {"status": "OK", "http_status": status_code, "top_keys": list(data.keys())[:10]}
    (EXPORTS_DIR / "ebay_get_opted_in_programs_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("GET_OPTED_IN_PROGRAMS_OK")
    print("http_status =", status_code)
    print("top_keys =", list(data.keys())[:10])

if __name__ == "__main__":
    main()
