import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
AUDIT_PATH = BASE_DIR / "storage" / "exports" / "adapter_001_live_specifics_revise_audit_v2.json"
def main():
    data = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
    body = data.get("response_body", {})
    print("ADAPTER_001_ERROR_BODY_AUDIT")
    print("status =", data.get("status"))
    print("decision =", data.get("decision"))
    print("http_status =", data.get("http_status"))
    print("response_body =", json.dumps(body, ensure_ascii=False))
if __name__ == "__main__":
    main()
