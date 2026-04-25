import json
import requests
from pathlib import Path

PAYLOAD_FILE = Path("ebay_api_payload_v3.json")

# ⚠️ ВСТАВИ СЮДА СВОЙ SANDBOX TOKEN
ACCESS_TOKEN = "YOUR_SANDBOX_TOKEN_HERE"

SANDBOX_URL = "https://api.sandbox.ebay.com/sell/inventory/v1/inventory_item"


def main():
    if not PAYLOAD_FILE.exists():
        print("ERROR: payload not found")
        return

    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    print("SENDING TO EBAY SANDBOX...")

    response = requests.post(SANDBOX_URL, json=payload, headers=headers)

    print(f"STATUS: {response.status_code}")
    print("RESPONSE:")
    print(response.text)


if __name__ == "__main__":
    main()