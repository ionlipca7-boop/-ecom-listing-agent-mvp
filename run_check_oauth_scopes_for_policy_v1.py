from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
SECRETS = BASE_DIR / "storage" / "secrets"
OUT_PATH = BASE_DIR / "storage" / "exports" / "oauth_scopes_policy_check_v1.json"

def read_text_if_exists(path):
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore").strip()
    return ""

def main():
    scopes_path = SECRETS / "ebay_scopes.txt"
    raw = read_text_if_exists(scopes_path)
    normalized = raw.replace("%%20", " ").replace("%%2B", "+").replace("%%3A", ":").replace("%20", " ").replace("\n", " ").replace("\r", " ").strip()
    scopes = [x for x in normalized.split(" ") if x]
    has_sell_inventory = "https://api.ebay.com/oauth/api_scope/sell.inventory" in scopes
    has_sell_account = "https://api.ebay.com/oauth/api_scope/sell.account" in scopes
    has_sell_account_ro = "https://api.ebay.com/oauth/api_scope/sell.account.readonly" in scopes
    ready_for_policy_refresh = has_sell_account or has_sell_account_ro
    recommended_path = "refresh_existing_user_token_with_same_scopes" if ready_for_policy_refresh else "start_new_consent_flow_with_sell_account_scope"
    result = {
        "status": "OK",
        "decision": "oauth_scopes_policy_check_v1_completed",
        "scopes_file_exists": scopes_path.exists(),
        "scopes_count": len(scopes),
        "has_sell_inventory": has_sell_inventory,
        "has_sell_account": has_sell_account,
        "has_sell_account_readonly": has_sell_account_ro,
        "ready_for_policy_refresh": ready_for_policy_refresh,
        "recommended_path": recommended_path
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OAUTH_SCOPES_POLICY_CHECK_V1_AUDIT")
    print("status = OK")
    print("scopes_file_exists =", result["scopes_file_exists"])
    print("scopes_count =", result["scopes_count"])
    print("has_sell_inventory =", result["has_sell_inventory"])
    print("has_sell_account =", result["has_sell_account"])
    print("has_sell_account_readonly =", result["has_sell_account_readonly"])
    print("ready_for_policy_refresh =", result["ready_for_policy_refresh"])
    print("recommended_path =", result["recommended_path"])

if __name__ == "__main__":
    main()
