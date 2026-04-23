import json
import requests
from pathlib import Path
BASE = Path(__file__).resolve().parent
TOKEN_PATH = BASE / "storage" / "secrets" / "ebay_access_token.txt"
def get_token():
    return TOKEN_PATH.read_text(encoding="utf-8").strip()
def main():
    sku = "USBCOTGAdapterUSB3TypCaufUSBAq10p399"
    url = f"https://api.ebay.com/sell/inventory/v1/inventory_item/{sku}"
    payload = {
        "product": {
            "title": "USB-C auf USB-A Adapter OTG USB 3.0 Schnell Datenadapter fur Samsung MacBook",
            "description": "Kompakter USB-C auf USB-A Adapter mit OTG Funktion und USB 3.0 Geschwindigkeit. Perfekt fur Smartphones, Tablets und Laptops wie Samsung oder MacBook. Unterstutzt schnelle Datenubertragung und vielseitige Nutzung im Alltag.",
            "imageUrls": [
                "https://ae01.alicdn.com/kf/S42fabc33d69c4f5592466804c540a072T.jpg",
                "https://ae01.alicdn.com/kf/Sc68f16cdbb0e48ca9f68da607d90f55fO.jpg",
                "https://ae01.alicdn.com/kf/Sceae79ed63dc4d5aab039de4a52879c8r.jpg",
                "https://ae01.alicdn.com/kf/S8893d5727a1446bb860b97548ede5410X.jpg",
                "https://ae01.alicdn.com/kf/S4f8750a0169946e0b4fc1a0f1b23089aB.jpg",
                "https://ae01.alicdn.com/kf/S3a9306f37bbf44d28dcc5d7b5aaa5c7bl.jpg",
                "https://ae01.alicdn.com/kf/Sadcd253f429a49b8a3460fe75febf721R.jpg"
            ],
            "aspects": {
                "Produktart": ["USB-C auf USB-A Adapter"],
                "Kompatibel mit": ["Samsung", "MacBook", "Android Gerate"]
            }
        }
    }
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "Content-Type": "application/json",
        "Content-Language": "de-DE"
    }
    r = requests.put(url, headers=headers, json=payload)
    print("LIVE_INVENTORY_REVISE")
    print("http_status =", r.status_code)
    try:
        print("response =", r.json())
    except:
        print("response_text =", r.text)
if __name__ == "__main__":
    main()
