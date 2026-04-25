import json, pathlib, datetime, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = ROOT / ".env.local"
OUT = ROOT / "storage" / "ebay" / "sell_inventory_items_read_only_v1.json"
API_URL = "https://api.ebay.com/sell/inventory/v1/inventory_item?limit=200"

def clean_value(v):
    return v.strip().strip(chr(34)).strip(chr(39))

def load_env(path):
    data = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                data[k.strip()] = clean_value(v)
    return data

def main():
    env = load_env(ENV)
    token = env.get("EBAY_ACCESS_TOKEN")
    if not token:
        raise SystemExit("BLOCKED: missing EBAY_ACCESS_TOKEN")
    headers = {"Authorization": "Bearer " + token, "Accept": "application/json", "Content-Type": "application/json"}
    r = requests.get(API_URL, headers=headers, timeout=45)
    try:
        body = r.json()
    except Exception:
        body = {"raw_text": r.text}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"status": "OK" if r.ok else "HTTP_ERROR", "layer": "SELL_INVENTORY_READ_ONLY_FETCHER_V1", "http_status": r.status_code, "read_only": True, "publish_called": False, "revise_called": False, "delete_called": False, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "body": body}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(OUT))

if __name__ == "__main__":
    main()
