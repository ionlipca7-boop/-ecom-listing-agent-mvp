import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TOKEN_PATH = BASE_DIR / "storage" / "secrets" / "ebay_access_token.txt"
OUTPUT_PATH = BASE_DIR / "storage" / "exports" / "ebay_access_token_audit_v1.json"

def main():
    exists = TOKEN_PATH.exists()
    raw = TOKEN_PATH.read_text(encoding="utf-8") if exists else ""
    token = raw.strip()
    result = {
        "status": "OK",
        "decision": "token_present" if token else "token_missing_or_empty",
        "file_exists": exists,
        "token_length": len(token),
        "starts_with": token[:20],
        "has_bom_in_raw": raw.startswith("\ufeff"),
        "has_whitespace_edges": raw != token,
        "looks_like_user_token": "v^1.1#" in token,
        "looks_like_access_token": len(token) > 200 and "v^1.1#" not in token
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ACCESS_TOKEN_AUDIT_V1")
    print("file_exists =", result["file_exists"])
    print("token_length =", result["token_length"])
    print("starts_with =", repr(result["starts_with"]))
    print("has_bom_in_raw =", result["has_bom_in_raw"])
    print("looks_like_user_token =", result["looks_like_user_token"])
    print("looks_like_access_token =", result["looks_like_access_token"])

if __name__ == "__main__":
    main()
