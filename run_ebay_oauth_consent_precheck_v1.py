import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
CLIENT_ID_PATH = SECRETS_DIR / "ebay_client_id.txt"
RU_NAME_PATH = SECRETS_DIR / "ebay_ru_name.txt"
STATE_PATH = SECRETS_DIR / "ebay_oauth_state_v1.txt"
OUTPUT_PATH = EXPORTS_DIR / "ebay_oauth_consent_precheck_v1.json"

def read_text_if_exists(path):
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""

def main():
    client_id = read_text_if_exists(CLIENT_ID_PATH)
    ru_name = read_text_if_exists(RU_NAME_PATH)
    missing = []
    if not CLIENT_ID_PATH.exists():
        missing.append("ebay_client_id.txt")
    if not RU_NAME_PATH.exists():
        missing.append("ebay_ru_name.txt")
    if CLIENT_ID_PATH.exists() and not client_id:
        missing.append("ebay_client_id.txt_empty")
    if RU_NAME_PATH.exists() and not ru_name:
        missing.append("ebay_ru_name.txt_empty")
    is_ready = not missing
    result = {
        "status": "OK",
        "decision": "oauth_consent_ready" if is_ready else "missing_oauth_inputs",
        "is_ready": is_ready,
        "missing": missing,
        "client_id_exists": CLIENT_ID_PATH.exists(),
        "ru_name_exists": RU_NAME_PATH.exists(),
        "client_id_prefix": client_id[:12],
        "ru_name_value": ru_name,
        "state_file_path": str(STATE_PATH)
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("EBAY_OAUTH_CONSENT_PRECHECK_V1")
    print("is_ready =", is_ready)
    print("missing =", missing)
    print("client_id_exists =", CLIENT_ID_PATH.exists())
    print("ru_name_exists =", RU_NAME_PATH.exists())

if __name__ == "__main__":
    main()
