import requests

TOKEN = "8773754337:AAGtcjTvtMoAtcigvAGRxjRYrgVn9LoQSnQ".strip()
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def call(method, params=None, timeout=20):
    url = f"{BASE_URL}/{method}"
    r = requests.get(url, params=params, timeout=timeout)
    print("METHOD:", method)
    print("HTTP STATUS:", r.status_code)
    try:
        print("JSON:", r.json())
    except Exception:
        print("RAW:", r.text)
    print("-" * 50)

call("getMe")
call("getUpdates", {"timeout": 1})