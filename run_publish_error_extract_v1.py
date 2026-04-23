import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILES = [
    BASE_DIR / "storage" / "exports" / "full_publish_pipeline_v2_audit.json",
    BASE_DIR / "storage" / "exports" / "publish_existing_offer_repair_v1.json"
]

def main():
    print("PUBLISH_ERROR_EXTRACT")
    for path in FILES:
        if not path.exists():
            print("file_missing =", path.name)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        print("file =", path.name)
        print("status =", data.get("status"))
        print("decision =", data.get("decision"))
        print("offerId =", data.get("offerId"))
        print("publish_http_status =", data.get("publish_http_status"))
        print("publish_response =")
        print(json.dumps(data.get("publish_response", data.get("publish_response_text")), ensure_ascii=False, indent=2))
        print("---")

if __name__ == "__main__":
    main()
