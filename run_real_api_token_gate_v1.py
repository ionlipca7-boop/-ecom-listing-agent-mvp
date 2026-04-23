import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "storage" / "exports" / "ebay_access_token_audit_v1.json"
OUTPUT_PATH = BASE_DIR / "storage" / "exports" / "real_api_token_gate_v1.json"

def main():
    data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    looks_like_user_token = data.get("looks_like_user_token", False)
    looks_like_access_token = data.get("looks_like_access_token", False)
    token_length = data.get("token_length", 0)
    is_ready = looks_like_access_token and not looks_like_user_token
    if is_ready:
        decision = "real_api_allowed"
    else:
        decision = "restore_oauth_access_token_required"
    result = {
        "status": "OK",
        "decision": decision,
        "is_ready": is_ready,
        "reason": "user_token_detected_in_access_token_file" if looks_like_user_token else "access_token_not_confirmed",
        "token_length": token_length,
        "next_step": "restore_valid_oauth_access_token_via_consent_flow"
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("REAL_API_TOKEN_GATE_V1")
    print("is_ready =", is_ready)
    print("decision =", decision)
    print("reason =", result["reason"])

if __name__ == "__main__":
    main()
