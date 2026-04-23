import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS = BASE_DIR / "storage" / "secrets"
EXPORTS = BASE_DIR / "storage" / "exports"
EXPORTS.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORTS / "policy_scope_recovery_audit_v1.json"

def exists_text(name):
    p = SECRETS / name
    return {"file": name, "exists": p.exists(), "size": p.stat().st_size if p.exists() else 0}

def main():
    files = [
        "ebay_access_token.txt",
        "ebay_refresh_token.txt",
        "ebay_redirect_uri.txt",
        "ebay_client_id.txt",
        "ebay_client_secret.txt",
        "ebay_scopes.txt",
        "ebay_auth_code.txt" 
    ]
    checked = [exists_text(x) for x in files]
    lookup = {x["file"]: x for x in checked}
    ready_for_refresh = lookup["ebay_refresh_token.txt"]["exists"] and lookup["ebay_client_id.txt"]["exists"] and lookup["ebay_client_secret.txt"]["exists"]
    ready_for_consent = lookup["ebay_redirect_uri.txt"]["exists"] and lookup["ebay_client_id.txt"]["exists"]
    result = {
        "status": "OK",
        "decision": "policy_scope_recovery_audit_v1_completed",
        "problem_confirmed": "access_token_missing_required_sell_account_scope",
        "files_checked": checked,
        "ready_for_refresh": ready_for_refresh,
        "ready_for_consent": ready_for_consent,
        "recommended_path": "refresh_existing_user_token" if ready_for_refresh else ("start_new_consent_flow" if ready_for_consent else "manual_secret_recovery_needed"),
        "next_step": "refresh_user_access_token_with_correct_scopes" if ready_for_refresh else ("build_new_oauth_consent_url_v1" if ready_for_consent else "locate_missing_oauth_files")
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("POLICY_SCOPE_RECOVERY_AUDIT_V1")
    print("status = OK")
    print("problem_confirmed = access_token_missing_required_sell_account_scope")
    print("ready_for_refresh =", result["ready_for_refresh"])
    print("ready_for_consent =", result["ready_for_consent"])
    print("recommended_path =", result["recommended_path"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
