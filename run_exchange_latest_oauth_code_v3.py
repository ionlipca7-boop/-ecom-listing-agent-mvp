import json
import base64
import requests
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
SECRETS = ROOT / "storage" / "secrets"
EXPORTS = ROOT / "storage" / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)
SECRETS.mkdir(parents=True, exist_ok=True)

redirected_url = r"https://auth2.ebay.com/oauth2/ThirdPartyAuthSucessFailure?isAuthSuccessful=true^&code=v%%5E1.1%%23i%%5E1%%23f%%5E0%%23r%%5E1%%23p%%5E3%%23I%%5E3%%23t%%5EUl41XzA6MEVFMDk0RjZFMEI3RURDQUJGRUNEQzdDNUFGQjVGODlfMF8xI0VeMjYw^&expires_in=299"
client_id_path = SECRETS / "ebay_client_id.txt"
client_secret_path = SECRETS / "ebay_client_secret.txt"
redirect_uri_path = SECRETS / "ebay_redirect_uri.txt"
access_token_out = SECRETS / "ebay_user_access_token.txt"
refresh_token_out = SECRETS / "ebay_refresh_token.txt"
result_out = EXPORTS / "oauth_user_token_exchange_v3.json"

result = {}
missing = []
if not client_id_path.exists(): missing.append("ebay_client_id.txt")
if not client_secret_path.exists(): missing.append("ebay_client_secret.txt")
if not redirect_uri_path.exists(): missing.append("ebay_redirect_uri.txt")

if missing:
    result["status"] = "ERROR"
    result["decision"] = "missing_required_secret_files"
    result["missing_files"] = missing
else:
    client_id = client_id_path.read_text(encoding="utf-8").strip()
    client_secret = client_secret_path.read_text(encoding="utf-8").strip()
    redirect_uri = redirect_uri_path.read_text(encoding="utf-8").strip()
    parsed = urlparse(redirected_url)
    raw_code = parse_qs(parsed.query).get("code", [""])[0]
    basic = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + basic}
    data = {"grant_type": "authorization_code", "code": raw_code, "redirect_uri": redirect_uri}
    response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data, timeout=60)
    try:
        response_json = response.json()
    except Exception:
        response_json = {"raw_text": response.text}
    result["status"] = "OK" if response.status_code == 200 else "ERROR"
    result["decision"] = "oauth_user_token_exchange_v3_completed"
    result["http_status"] = response.status_code
    result["code_found"] = bool(raw_code)
    result["code_prefix"] = raw_code[:20] if raw_code else "" 
    result["access_token_present"] = bool(response_json.get("access_token")) if isinstance(response_json, dict) else False
    result["refresh_token_present"] = bool(response_json.get("refresh_token")) if isinstance(response_json, dict) else False
    result["response_preview"] = response_json
    if response.status_code == 200 and isinstance(response_json, dict):
        access_token_out.write_text(response_json.get("access_token", ""), encoding="utf-8")
        if response_json.get("refresh_token"): refresh_token_out.write_text(response_json.get("refresh_token"), encoding="utf-8")

result_out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("OAUTH_USER_TOKEN_EXCHANGE_V3_FINAL_AUDIT")
print("status =", result.get("status"))
print("decision =", result.get("decision"))
print("http_status =", result.get("http_status", "-"))
print("code_found =", result.get("code_found", False))
print("access_token_present =", result.get("access_token_present", False))
print("refresh_token_present =", result.get("refresh_token_present", False))
print("next_step = fetch_real_policy_ids_if_http_200")
