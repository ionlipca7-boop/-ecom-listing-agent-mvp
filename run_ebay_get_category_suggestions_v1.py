import base64
import json
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def read_secret(name):
    return (SECRETS_DIR / name).read_text(encoding="utf-8-sig").strip()

def get_app_token(client_id, client_secret):
    basic = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
    form = urllib.parse.urlencode({"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope"}).encode("utf-8")
    req = urllib.request.Request("https://api.ebay.com/identity/v1/oauth2/token", data=form, headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + basic}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8")).get("access_token", "")

def api_get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token, "Accept": "application/json", "Accept-Language": "de-DE"}, method="GET")
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode("utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    client_id = read_secret("ebay_client_id.txt")
    client_secret = read_secret("ebay_client_secret.txt")
    query = "USB-C Ladekabel 2m 60W"
    app_token = get_app_token(client_id, client_secret)
    status_tree, tree_data = api_get("https://api.ebay.com/commerce/taxonomy/v1/get_default_category_tree_id?marketplace_id=EBAY_DE", app_token)
    tree_id = tree_data.get("categoryTreeId")
    sug_url = "https://api.ebay.com/commerce/taxonomy/v1/category_tree/" + tree_id + "/get_category_suggestions?q=" + urllib.parse.quote(query)
    status_sug, sug_data = api_get(sug_url, app_token)
    suggestions = sug_data.get("categorySuggestions", [])
    first = suggestions[0] if suggestions else {}
    first_cat = first.get("category", {}) if first else {}
    audit = {
        "status": "OK",
        "categoryTreeId": tree_id,
        "suggestion_count": len(suggestions),
        "top_categoryId": first_cat.get("categoryId"),
        "top_categoryName": first_cat.get("categoryName")
    }
    (EXPORTS_DIR / "ebay_category_suggestions_audit_v1.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print("GET_CATEGORY_SUGGESTIONS_OK")
    print("categoryTreeId =", tree_id)
    print("suggestion_count =", len(suggestions))
    print("top_categoryId =", first_cat.get("categoryId"))
    print("top_categoryName =", first_cat.get("categoryName"))

if __name__ == "__main__":
    main()
