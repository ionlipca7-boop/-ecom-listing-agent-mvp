import os, json, pathlib, datetime, requests

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "storage" / "ebay" / "trading_active_listings_read_only_v1.json"
ENV = ROOT / ".env.local"

API_URL = "https://api.ebay.com/ws/api.dll"
CALL_NAME = "GetMyeBaySelling"
SITE_ID = "77"
COMPAT_LEVEL = "1193"


def load_env(path):
    data = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                data[k.strip()] = v.strip().strip(chr(34)+chr(39))
    return data


def main():
    env = load_env(ENV)
    token = env.get("EBAY_ACCESS_TOKEN") or env.get("EBAY_AUTH_TOKEN") or env.get("EBAY_USER_TOKEN") or os.getenv("EBAY_ACCESS_TOKEN") or os.getenv("EBAY_AUTH_TOKEN") or os.getenv("EBAY_USER_TOKEN")
    if not token:
        raise SystemExit("BLOCKED: missing EBAY_AUTH_TOKEN / EBAY_USER_TOKEN")
    xml = f"""<?xml version='1.0' encoding='utf-8'?><GetMyeBaySellingRequest xmlns='urn:ebay:apis:eBLBaseComponents'><RequesterCredentials><eBayAuthToken>{token}</eBayAuthToken></RequesterCredentials><ActiveList><Include>true</Include><IncludeNotes>false</IncludeNotes><Pagination><EntriesPerPage>200</EntriesPerPage><PageNumber>1</PageNumber></Pagination></ActiveList><DetailLevel>ReturnAll</DetailLevel></GetMyeBaySellingRequest>"""
    headers = {"X-EBAY-API-CALL-NAME": CALL_NAME, "X-EBAY-API-SITEID": SITE_ID, "X-EBAY-API-COMPATIBILITY-LEVEL": COMPAT_LEVEL, "X-EBAY-API-REQUEST-ENCODING": "XML", "Content-Type": "text/xml"}
    r = requests.post(API_URL, headers=headers, data=xml.encode("utf-8"), timeout=45)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"status": "OK" if r.ok else "HTTP_ERROR", "layer": "TRADING_API_GET_MY_EBAY_SELLING_READ_ONLY_V1", "http_status": r.status_code, "read_only": True, "publish_called": False, "revise_called": False, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "raw_xml": r.text}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(OUT))


if __name__ == "__main__":
    main()
