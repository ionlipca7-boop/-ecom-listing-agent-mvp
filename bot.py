import json
import os
import time
from pathlib import Path

import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN is missing. Set it as a server environment variable, never commit it to GitHub.")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
ROOT = Path(__file__).resolve().parent
RUNTIME_STATE = ROOT / "storage" / "runtime" / "current_runtime_state_v1.json"
APPROVAL_PACKET = ROOT / "storage" / "approval" / "first_listing_telegram_approval_packet_v1.json"
CONTROL_ACTION = ROOT / "storage" / "control_action.json"

offset = 0


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "MISSING_OR_INVALID", "path": str(path), "error": str(exc)}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def send_message(chat_id: int, text: str, reply_markup: dict | None = None) -> None:
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
    requests.post(f"{BASE_URL}/sendMessage", data=payload, timeout=20)


def build_status_text() -> str:
    state = read_json(RUNTIME_STATE)
    return "\n".join([
        "ECOM CONTROL ROOM STATUS",
        f"status: {state.get('status')}",
        f"telegram: {state.get('telegram_bot') or state.get('telegram_username')}",
        f"server: {state.get('server_runtime')}",
        f"github_branch: {state.get('github_branch')}",
        f"publish_allowed: {state.get('publish_allowed', False)}",
        f"auto_publish_allowed: {state.get('auto_publish_allowed', False)}",
        f"next: {state.get('next_allowed_action')}",
    ])


def build_approval_text() -> str:
    packet = read_json(APPROVAL_PACKET)
    listing = packet.get("listing") or packet.get("payload") or packet
    return "\n".join([
        "FIRST LISTING APPROVAL",
        f"status: {packet.get('status')}",
        f"title: {listing.get('title')}",
        f"sku: {listing.get('sku')}",
        f"price: {listing.get('price')}",
        f"quantity: {listing.get('quantity')}",
        "",
        "Approve only if the listing is correct.",
        "Publish still requires token guard before any eBay write.",
    ])


def handle_text(chat_id: int, text: str) -> None:
    normalized = (text or "").strip().lower()

    if normalized in {"/start", "start"}:
        send_message(chat_id, "ECOM Agent connected. Use /status, /approval, /auto, /help.")
        return

    if normalized in {"/help", "help"}:
        send_message(chat_id, "Commands: /status, /approval, /auto, /approve, /reject. Auto publish is locked until a later gate.")
        return

    if normalized in {"/status", "status"}:
        send_message(chat_id, build_status_text())
        return

    if normalized in {"/approval", "approval"}:
        buttons = {"inline_keyboard": [[{"text": "APPROVE", "callback_data": "APPROVE_FIRST_LISTING"}, {"text": "REJECT", "callback_data": "REJECT_FIRST_LISTING"}], [{"text": "STATUS", "callback_data": "STATUS"}]]}
        send_message(chat_id, build_approval_text(), buttons)
        return

    if normalized in {"/auto", "auto"}:
        send_message(chat_id, "AUTO MODE: locked. Current mode is approval-first. No batch publish, no auto publish.")
        return

    if normalized in {"/approve", "approve"}:
        write_json(CONTROL_ACTION, {"status": "PENDING_TOKEN_GUARD", "action": "APPROVE_FIRST_LISTING", "source": "telegram_text_command", "publish_allowed": False})
        send_message(chat_id, "Approval recorded. Token guard must run before one real eBay publish.")
        return

    if normalized in {"/reject", "reject"}:
        write_json(CONTROL_ACTION, {"status": "REJECTED", "action": "REJECT_FIRST_LISTING", "source": "telegram_text_command", "publish_allowed": False})
        send_message(chat_id, "Listing rejected. No publish will run.")
        return

    send_message(chat_id, "Unknown command. Use /status, /approval, /auto, /help.")


def handle_callback(callback: dict) -> None:
    message = callback.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    data = callback.get("data")
    if not chat_id:
        return

    if data == "STATUS":
        send_message(chat_id, build_status_text())
    elif data == "APPROVE_FIRST_LISTING":
        write_json(CONTROL_ACTION, {"status": "PENDING_TOKEN_GUARD", "action": "APPROVE_FIRST_LISTING", "source": "telegram_button", "publish_allowed": False})
        send_message(chat_id, "Approval recorded. Token guard required before one real eBay publish.")
    elif data == "REJECT_FIRST_LISTING":
        write_json(CONTROL_ACTION, {"status": "REJECTED", "action": "REJECT_FIRST_LISTING", "source": "telegram_button", "publish_allowed": False})
        send_message(chat_id, "Rejected. No publish will run.")


def main() -> None:
    global offset
    print("ECOM CONTROL ROOM TELEGRAM BOT STARTED")
    while True:
        try:
            response = requests.get(f"{BASE_URL}/getUpdates", params={"timeout": 30, "offset": offset + 1}, timeout=35)
            data = response.json()
            if not data.get("ok"):
                print("TELEGRAM ERROR:", data)
                time.sleep(3)
                continue
            for update in data.get("result", []):
                offset = update["update_id"]
                if "callback_query" in update:
                    handle_callback(update["callback_query"])
                    continue
                message = update.get("message") or {}
                chat = message.get("chat") or {}
                chat_id = chat.get("id")
                if chat_id:
                    handle_text(chat_id, message.get("text", ""))
        except Exception as exc:
            print("RUNTIME ERROR:", exc)
            time.sleep(3)


if __name__ == "__main__":
    main()
