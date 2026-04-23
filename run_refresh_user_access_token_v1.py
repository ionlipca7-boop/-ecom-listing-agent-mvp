import json
import base64
import requests
from pathlib import Path

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
SECRETS = ROOT / "storage" / "secrets"
EXPORTS = ROOT / "storage" / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)

client_id_path = SECRETS / "ebay_client_id.txt"
client_secret_path = SECRETS / "ebay_client_secret.txt"
refresh_token_path = SECRETS / "ebay_refresh_token.txt"
access_token_out = SECRETS / "ebay_access_token.txt"
result_out = EXPORTS / "refresh_user_access_token_v1.json"

result = {}
missing = []
if not client_id_path.exists(): missing.append("ebay_client_id.txt")
if not client_secret_path.exists(): missing.append("ebay_client_secret.txt")
if not refresh_token_path.exists(): missing.append("ebay_refresh_token.txt")

if missing:
    result["status"] = "ERROR"
    result["decision"] = "missing_required_secret_files"
    result["missing_files"] = missing
else:
    client_id = client_id_path.read_text(encoding="utf-8").strip()
    client_secret = client_secret_path.read_text(encoding="utf-8").strip()
    refresh_token = refresh_token_path.read_text(encoding="utf-8").strip()
    scopes = [
        "https://api.ebay.com/oauth/api_scope",
        "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.account",
        "https://api.ebay.com/oauth/api_scope/sell.account.readonly"
    ]
    basic = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + basic}
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token, "scope": " ".join(scopes)}
    response = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data, timeout=60)
    try:
        response_json = response.json()
    except Exception:
        response_json = {"raw_text": response.text}
    result["status"] = "OK" if response.status_code == 200 else "ERROR"
    result["decision"] = "refresh_user_access_token_v1_completed"
    result["http_status"] = response.status_code
    result["access_token_present"] = bool(response_json.get("access_token")) if isinstance(response_json, dict) else False
    result["token_type"] = response_json.get("token_type") if isinstance(response_json, dict) else None
    result["expires_in"] = response_json.get("expires_in") if isinstance(response_json, dict) else None
    result["response_preview"] = response_json
    if response.status_code == 200 and isinstance(response_json, dict) and response_json.get("access_token"):
        access_token_out.write_text(response_json.get("access_token"), encoding="utf-8")

result_out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("REFRESH_USER_ACCESS_TOKEN_V1_FINAL_AUDIT")
print("status =", result.get("status"))
print("decision =", result.get("decision"))
print("http_status =", result.get("http_status", "-"))
print("access_token_present =", result.get("access_token_present", False))
print("token_type =", result.get("token_type", "-"))
print("next_step = fetch_real_policy_ids_if_http_200")
