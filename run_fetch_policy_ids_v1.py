import json
from pathlib import Path

try:
    import requests
except Exception as e:
    print("ERROR_IMPORT_REQUESTS")
    print(e)
    exit()

BASE_DIR = Path(__file__).resolve().parent
TOKEN_PATH = BASE_DIR / "storage" / "secrets" / "ebay_access_token.txt"
OUT_PATH = BASE_DIR / "storage" / "exports" / "policy_ids_v1.json"

print("STEP_1_TOKEN_CHECK")
print("token_exists =", TOKEN_PATH.exists())

if not TOKEN_PATH.exists():
    print("ERROR: TOKEN NOT FOUND")
    exit()

token = TOKEN_PATH.read_text(encoding="utf-8").strip()

headers = {
    "Authorization": "Bearer " + token,
    "Accept": "application/json",
    "Content-Language": "de-DE"
}

url = "https://api.ebay.com/sell/account/v1/fulfillment_policy?marketplace_id=EBAY_DE"

print("STEP_2_API_CALL")

try:
    r = requests.get(url, headers=headers, timeout=30)
    print("http_status =", r.status_code)
    print("response_preview =", r.text[:200])
except Exception as e:
    print("ERROR_API_CALL")
    print(e)
    exit()

print("STEP_3_WRITE_FILE")
OUT_PATH.write_text("TEST_OK", encoding="utf-8")
print("file_created =", OUT_PATH.exists())
