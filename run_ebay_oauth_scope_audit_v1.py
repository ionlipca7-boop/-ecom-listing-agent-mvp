import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
CONSENT_FILE = BASE_DIR / "storage" / "exports" / "ebay_oauth_consent_url_v1.txt"

def main():
    text = CONSENT_FILE.read_text(encoding="utf-8").strip()
    parsed = urllib.parse.urlparse(text)
    qs = urllib.parse.parse_qs(parsed.query)
    raw_scope = qs.get("scope", [""])[0]
    scopes = [x for x in raw_scope.split(" ") if x]
    print("OAUTH_SCOPE_AUDIT")
    print("scope_count =", len(scopes))
    print("has_sell_inventory =", "https://api.ebay.com/oauth/api_scope/sell.inventory" in scopes)
    print("has_sell_account =", "https://api.ebay.com/oauth/api_scope/sell.account" in scopes)
    print("scopes =")
    for s in scopes:
        print(s)

if __name__ == "__main__":
    main()
