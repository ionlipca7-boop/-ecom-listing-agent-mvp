import json
import urllib.parse
from pathlib import Path

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
SECRETS = ROOT / "storage" / "secrets"
EXPORTS = ROOT / "storage" / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)

client_id_path = SECRETS / "ebay_client_id.txt"
redirect_uri_path = SECRETS / "ebay_redirect_uri.txt"
out = EXPORTS / "new_oauth_consent_url_v1.json"
result = {}

if not client_id_path.exists() or not redirect_uri_path.exists():
    result["status"] = "ERROR"
    result["decision"] = "missing_secrets"
    result["client_id_exists"] = client_id_path.exists()
    result["redirect_uri_exists"] = redirect_uri_path.exists()
else:
    client_id = client_id_path.read_text(encoding="utf-8").strip()
    redirect_uri = redirect_uri_path.read_text(encoding="utf-8").strip()
    scopes = [
        "https://api.ebay.com/oauth/api_scope",
        "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.account",
        "https://api.ebay.com/oauth/api_scope/sell.account.readonly"
    ]
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes)
    }
    consent_url = "https://auth.ebay.com/oauth2/authorize?" + urllib.parse.urlencode(params)
    result["status"] = "OK"
    result["decision"] = "consent_url_built"
    result["scope_count"] = len(scopes)
    result["has_sell_account"] = True
    result["has_sell_account_readonly"] = True
    result["consent_url"] = consent_url
    result["next_step"] = "open_consent_url_and_capture_auth_code"

out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("NEW_OAUTH_CONSENT_URL_V1_FINAL_AUDIT")
print("status =", result.get("status"))
print("decision =", result.get("decision"))
print("file_created =", out.exists())
print("script_exists =", Path("run_oauth_fix_v1.py").exists())
print("next_step =", result.get("next_step", "-"))
