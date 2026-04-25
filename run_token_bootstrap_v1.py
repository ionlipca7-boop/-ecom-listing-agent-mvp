import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "token_bootstrap_v1.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    refresh_run = subprocess.run(["python", "run_ebay_refresh_access_token_v2.py"])
    refresh_audit = read_json(EXPORTS_DIR / "ebay_refresh_access_token_audit_v2.json")
    refresh_ok = refresh_audit.get("status") == "OK" and refresh_audit.get("http_status") == 200
    quantity_status = "SKIPPED"
    quantity_http_status = None
    if refresh_ok:
        subprocess.run(["python", "run_increase_live_quantity_v1.py"])
        qty_audit = read_json(EXPORTS_DIR / "ebay_increase_live_quantity_audit_v1.json")
        quantity_status = qty_audit.get("status")
        quantity_http_status = qty_audit.get("http_status")
    result = {"status": "OK" if refresh_ok and quantity_status == "OK" else "FAILED", "refresh_exit_code": refresh_run.returncode, "refresh_status": refresh_audit.get("status"), "refresh_http_status": refresh_audit.get("http_status"), "refresh_access_token_length": refresh_audit.get("access_token_length"), "quantity_status": quantity_status, "quantity_http_status": quantity_http_status}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TOKEN_BOOTSTRAP_V1_DONE")
    print("refresh_status =", refresh_audit.get("status"))
    print("refresh_http_status =", refresh_audit.get("http_status"))
    print("quantity_status =", quantity_status)
    print("quantity_http_status =", quantity_http_status)

if __name__ == "__main__":
    main()
