import json
from datetime import datetime, UTC
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
BASE_DIR = Path(__file__).resolve().parent
TOKEN_FILE = BASE_DIR / "storage" / "secrets" / "ebay_user_token.txt"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORT_DIR / "ebay_token_smoke_test_v2.json"
URL = "https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_DE&limit=1"
def interpret_status(code):
    if code == 200:
        return "TOKEN_OK_OR_NO_POLICIES"
    if code == 400:
        return "BAD_REQUEST"
    if code == 401:
        return "TOKEN_INVALID_OR_EXPIRED"
    if code == 403:
        return "SCOPE_OR_ACCOUNT_PERMISSION_ISSUE"
    if code is None:
        return "NO_HTTP_RESPONSE"
    return "UNKNOWN"
def main():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    result = {}
    result["checked_at"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    result["url"] = URL
    result["status_code"] = None
    result["interpretation"] = ""
    result["error"] = ""
    result["token_file_exists"] = TOKEN_FILE.exists()
    if not TOKEN_FILE.exists():
        result["interpretation"] = "TOKEN_FILE_MISSING"
        OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(result)
        return
    token = TOKEN_FILE.read_text(encoding="utf-8-sig").strip()
    result["token_length"] = len(token)
    if not token:
        result["interpretation"] = "TOKEN_FILE_EMPTY"
        OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(result)
        return
    req = Request(URL)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/json")
    try:
        resp = urlopen(req, timeout=30)
        code = resp.getcode()
        body = resp.read().decode("utf-8", errors="replace")
        result["status_code"] = code
        result["interpretation"] = interpret_status(code)
        result["response_preview"] = body[:500]
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        result["status_code"] = e.code
        result["interpretation"] = interpret_status(e.code)
        result["error"] = str(e)
        result["response_preview"] = body[:500]
    except URLError as e:
        result["error"] = "URLError: " + str(e)
    except Exception as e:
        result["error"] = str(e)
    OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(result)
if __name__ == "__main__":
    main()
