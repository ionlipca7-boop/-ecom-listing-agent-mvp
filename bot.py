import time
import requests

TOKEN = "8773754337:AAGtcjTvtMoAtcigvAGRxjRYrgVn9LoQSnQ".strip()
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

offset = 0

print("ECHO BOT STARTED")

while True:
    try:
        response = requests.get(
            f"{BASE_URL}/getUpdates",
            params={"timeout": 30, "offset": offset + 1},
            timeout=35
        )
        data = response.json()

        if not data.get("ok"):
            print("ERROR:", data)
            time.sleep(3)
            continue

        for update in data.get("result", []):
            offset = update["update_id"]

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            # --- ЛОГИКА ---
            if text.startswith("/start"):
                reply = "Bot is working ✅"
            elif text.startswith("/help"):
                reply = "Commands:\n/start\n/help"
            else:
                reply = f"ECHO: {text}"

            requests.get(
                f"{BASE_URL}/sendMessage",
                params={"chat_id": chat_id, "text": reply},
                timeout=20
            )

            print("IN:", text)
            print("OUT:", reply)

    except Exception as e:
        print("RUNTIME ERROR:", e)
        time.sleep(3)