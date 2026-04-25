import base64, json, pathlib, datetime, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENV = ROOT / ".env.local"
OUT = ROOT / "storage" / "ebay" / "token_refresh_result_safe_v1.json"
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
SCOPES = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory"

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
    cid = env.get("EBAY_CLIENT_ID")
    sec = env.get("EBAY_CLIENT_SECRET")
    ref = env.get("EBAY_REFRESH_TOKEN")
    if not cid or not sec or not ref:
        raise SystemExit("BLOCKED: missing EBAY_CLIENT_ID / EBAY_CLIENT_SECRET / EBAY_REFRESH_TOKEN")
    basic = base64.b64encode((cid + ":" + sec).encode("utf-8")).decode("ascii")
    headers = {"Authorization": "Basic " + basic, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "refresh_token", "refresh_token": ref, "scope": SCOPES}
    r = requests.post(TOKEN_URL, headers=headers, data=data, timeout=45)
    try:
        body = r.json()
    except Exception:
        body = {"raw_text": r.text}
    safe = {"status": "OK" if r.ok else "HTTP_ERROR", "layer": "EBAY_TOKEN_REFRESH_TOOL_V1", "http_status": r.status_code, "has_access_token": isinstance(body, dict) and bool(body.get("access_token")), "token_type": body.get("token_type") if isinstance(body, dict) else None, "expires_in": body.get("expires_in") if isinstance(body, dict) else None, "error": body.get("error") if isinstance(body, dict) else None, "error_description": body.get("error_description") if isinstance(body, dict) else None, "secret_values_printed": False, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")
    if r.ok and isinstance(body, dict) and body.get("access_token"):
        lines = ENV.read_text(encoding="utf-8", errors="replace").splitlines()
        new_lines = [("EBAY_ACCESS_TOKEN=" + body.get("access_token")) if line.startswith("EBAY_ACCESS_TOKEN=") else line for line in lines]
        ENV.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(str(OUT))

if __name__ == "__main__":
    main()
