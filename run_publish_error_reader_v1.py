import json
from pathlib import Path

FILE_PATH = Path("storage") / "exports" / "ebay_publish_offer_audit_v4.json"

def main():
    data = json.loads(FILE_PATH.read_text(encoding="utf-8"))
    response_json = data.get("response_json") or {}
    errors = response_json.get("errors") or []
    print("PUBLISH_ERROR_READER_V1")
    print("status =", data.get("status"))
    print("http_status =", data.get("http_status"))
    print("offerId =", data.get("offerId"))
    print("error_count =", len(errors))
    if errors:
        first = errors[0]
        print("first_error_json =")
        print(json.dumps(first, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
