import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
API_URL = "https://api.ebay.com/sell/account/v1/privilege"

def main() -> None:
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()

    request = urllib.request.Request(
        API_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8", errors="replace")
            status_code = response.getcode()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        audit = {"status": "FAILED", "http_status": e.code, "body": body}
        (EXPORTS_DIR / "ebay_access_token_smoke_test_v3.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
        print("SMOKE_TEST_FAILED")
        print("http_status =", e.code)
        print(body)
        raise SystemExit(1)

    try:
        parsed = json.loads(body)
    except Exception:
        parsed = {"raw_body": body}

    audit = {"status": "OK", "http_status": status_code, "body": parsed}
    (EXPORTS_DIR / "ebay_access_token_smoke_test_v3.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")

    print("SMOKE_TEST_OK")
    print("http_status =", status_code)
    if isinstance(parsed, dict):
        print("top_keys =", list(parsed.keys())[:10])
    else:
        print("response_type =", type(parsed).__name__)

if __name__ == "__main__":
    main()
