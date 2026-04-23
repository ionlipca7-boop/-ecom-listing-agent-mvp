import json
import base64
import webbrowser
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
SECRETS = ROOT / "storage" / "secrets"
EXPORTS = ROOT / "storage" / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)
SECRETS.mkdir(parents=True, exist_ok=True)

consent_json = EXPORTS / "new_oauth_consent_url_v1.json"
client_id_path = SECRETS / "ebay_client_id.txt"
client_secret_path = SECRETS / "ebay_client_secret.txt"
redirect_uri_path = SECRETS / "ebay_redirect_uri.txt"
access_token_out = SECRETS / "ebay_user_access_token.txt"
refresh_token_out = SECRETS / "ebay_refresh_token.txt"
result_out = EXPORTS / "oauth_user_token_exchange_v2.json"

result = {}
missing = []
if not consent_json.exists(): missing.append("new_oauth_consent_url_v1.json")
if not client_id_path.exists(): missing.append("ebay_client_id.txt")
if not client_secret_path.exists(): missing.append("ebay_client_secret.txt")
if not redirect_uri_path.exists(): missing.append("ebay_redirect_uri.txt")

if missing:
    result["status"] = "ERROR"
    result["decision"] = "missing_required_files"
    result["missing_files"] = missing
else:
    consent_data = json.loads(consent_json.read_text(encoding="utf-8"))
    consent_url = consent_data.get("consent_url", "")
    client_id = client_id_path.read_text(encoding="utf-8").strip()
    client_secret = client_secret_path.read_text(encoding="utf-8").strip()
    redirect_uri = redirect_uri_path.read_text(encoding="utf-8").strip()
    print("OPEN_BROWSER_NOW = True")
    webbrowser.open(consent_url)
    redirected_url = input("PASTE_FULL_REDIRECTED_URL_HERE: ").strip()
    parsed = urlparse(redirected_url)
    qs = parse_qs(parsed.query)
    raw_code = qs.get("code", [""])[0]
    auth_code = unquote(raw_code)
    basic = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + basic}
    data = {"grant_type": "authorization_code", "code": auth_code, "redirect_uri": redirect_uri}
    response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data, timeout=60)
    try:
        response_json = response.json()
    except Exception:
        response_json = {"raw_text": response.text}
    result["status"] = "OK" if response.status_code == 200 else "ERROR"
    result["decision"] = "oauth_user_token_exchange_v2_completed"
    result["http_status"] = response.status_code
    result["access_token_present"] = bool(response_json.get("access_token")) if isinstance(response_json, dict) else False
    result["refresh_token_present"] = bool(response_json.get("refresh_token")) if isinstance(response_json, dict) else False
    result["response_preview"] = response_json
    if response.status_code == 200 and isinstance(response_json, dict):
        access_token_out.write_text(response_json.get("access_token", ""), encoding="utf-8")
        if response_json.get("refresh_token"): refresh_token_out.write_text(response_json.get("refresh_token"), encoding="utf-8")

result_out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("OAUTH_USER_TOKEN_EXCHANGE_V2_FINAL_AUDIT")
print("status =", result.get("status"))
print("decision =", result.get("decision"))
print("http_status =", result.get("http_status", "-"))
print("access_token_present =", result.get("access_token_present", False))
print("refresh_token_present =", result.get("refresh_token_present", False))
print("result_file_exists =", result_out.exists())
print("next_step = fetch_real_policy_ids_if_http_200")
