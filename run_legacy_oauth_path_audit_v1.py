import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
OUTPUT_PATH = BASE_DIR / "storage" / "exports" / "legacy_oauth_path_audit_v1.json"

def read_preview(name):
    path = SECRETS_DIR / name
    if not path.exists():
        return {"exists": False, "size": 0, "preview": ""}
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    return {"exists": True, "size": len(text), "preview": text[:80]}

def main():
    redirect_info = read_preview("ebay_redirect_uri.txt")
    refresh_info = read_preview("ebay_refresh_token.txt")
    access_info = read_preview("ebay_access_token.txt")
    redirect_ok = redirect_info["exists"] and bool(redirect_info["size"])
    refresh_ok = refresh_info["exists"] and bool(refresh_info["size"])
    is_ready_for_refresh = redirect_ok and refresh_ok
    decision = "legacy_refresh_path_ready" if is_ready_for_refresh else "legacy_refresh_inputs_missing"
    result = {
        "status": "OK",
        "decision": decision,
        "is_ready_for_refresh": is_ready_for_refresh,
        "redirect_uri": redirect_info,
        "refresh_token": refresh_info,
        "access_token": access_info
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("LEGACY_OAUTH_PATH_AUDIT_V1")
    print("is_ready_for_refresh =", is_ready_for_refresh)
    print("redirect_uri_exists =", redirect_info["exists"])
    print("redirect_uri_size =", redirect_info["size"])
    print("refresh_token_exists =", refresh_info["exists"])
    print("refresh_token_size =", refresh_info["size"])

if __name__ == "__main__":
    main()
