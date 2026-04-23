import json
from pathlib import Path
import requests

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_PATH = EXPORTS_DIR / "ebay_access_token_smoke_test_v4.json"

def main():
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_DE"
    }
    url = "https://api.ebay.com/sell/account/v1/privilege"
    r = requests.get(url, headers=headers, timeout=60)
    try:
        data = r.json()
    except Exception:
        data = {"raw_text": r.text[:1000]}
    result = {
        "status": "OK" if r.status_code == 200 else "FAILED",
        "http_status": r.status_code,
        "token_length": len(token),
        "response": data
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("EBAY_ACCESS_TOKEN_SMOKE_TEST_V4")
    print("http_status =", r.status_code)
    print("token_length =", len(token))

if __name__ == "__main__":
    main()
