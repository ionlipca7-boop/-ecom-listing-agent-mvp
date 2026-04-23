import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_PATH = EXPORTS_DIR / "system_snapshot_audit_v1.json"

def file_info(path):
    exists = path.exists()
    if not exists:
        return {"exists": False, "size": 0, "preview": ""}
    text = path.read_text(encoding="utf-8", errors="replace")
    preview = text[:120].replace("\n", "\\n")
    return {"exists": True, "size": len(text), "preview": preview}

def json_info(path):
    info = file_info(path)
    info["json_ok"] = False
    info["top_keys"] = []
    if info["exists"]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            info["json_ok"] = True
            if isinstance(data, dict):
                info["top_keys"] = list(data.keys())[:12]
        except Exception as e:
            info["json_error"] = str(e)
    return info

def py_info(path):
    info = file_info(path)
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    info["has_main"] = 'if __name__ == "__main__":' in text
    info["has_requests"] = "requests" in text
    info["has_output_path"] = "OUTPUT_PATH" in text
    return info

def main():
    audit = {
        "status": "OK",
        "decision": "system_snapshot_ready",
        "base_dir": str(BASE_DIR),
        "secrets": {
            "ebay_access_token.txt": file_info(SECRETS_DIR / "ebay_access_token.txt"),
            "ebay_client_id.txt": file_info(SECRETS_DIR / "ebay_client_id.txt"),
            "ebay_ru_name.txt": file_info(SECRETS_DIR / "ebay_ru_name.txt"),
            "ebay_oauth_state_v1.txt": file_info(SECRETS_DIR / "ebay_oauth_state_v1.txt")
        },
        "exports": {
            "real_offer_request_payload_v1.json": json_info(EXPORTS_DIR / "real_offer_request_payload_v1.json"),
            "real_offer_payload_gate_v1.json": json_info(EXPORTS_DIR / "real_offer_payload_gate_v1.json"),
            "ebay_policies_v1.json": json_info(EXPORTS_DIR / "ebay_policies_v1.json"),
            "ebay_access_token_audit_v1.json": json_info(EXPORTS_DIR / "ebay_access_token_audit_v1.json"),
            "real_api_token_gate_v1.json": json_info(EXPORTS_DIR / "real_api_token_gate_v1.json"),
            "ebay_oauth_consent_precheck_v1.json": json_info(EXPORTS_DIR / "ebay_oauth_consent_precheck_v1.json"),
            "ebay_oauth_consent_url_v1.json": json_info(EXPORTS_DIR / "ebay_oauth_consent_url_v1.json")
        },
        "scripts": {
            "run_real_offer_payload_gate_v1.py": py_info(BASE_DIR / "run_real_offer_payload_gate_v1.py"),
            "run_fetch_ebay_policies_v1.py": py_info(BASE_DIR / "run_fetch_ebay_policies_v1.py"),
            "run_access_token_audit_v1.py": py_info(BASE_DIR / "run_access_token_audit_v1.py"),
            "run_real_api_token_gate_v1.py": py_info(BASE_DIR / "run_real_api_token_gate_v1.py"),
            "run_ebay_oauth_consent_precheck_v1.py": py_info(BASE_DIR / "run_ebay_oauth_consent_precheck_v1.py"),
            "run_ebay_oauth_consent_url_v1.py": py_info(BASE_DIR / "run_ebay_oauth_consent_url_v1.py")
        }
    }
    OUTPUT_PATH.write_text(json.dumps(audit, indent=2, ensure_ascii=False), encoding="utf-8")
    print("SYSTEM_SNAPSHOT_AUDIT_V1")
    print("access_token_exists =", audit["secrets"]["ebay_access_token.txt"]["exists"])
    print("ru_name_exists =", audit["secrets"]["ebay_ru_name.txt"]["exists"])
    print("ru_name_size =", audit["secrets"]["ebay_ru_name.txt"]["size"])
    print("consent_url_json_exists =", audit["exports"]["ebay_oauth_consent_url_v1.json"]["exists"])

if __name__ == "__main__":
    main()
