import json
import os
from pathlib import Path
from typing import Any

import requests

PAYLOAD_PATH = Path("ebay_inventory_payload_v1.json")
CREDENTIALS_PATH = Path("ebay_sandbox_credentials_v1.json")
RESULT_PATH = Path("ebay_inventory_execution_v1.json")

DEFAULT_TIMEOUT_SECONDS = 15
DEFAULT_SANDBOX_URL = "https://api.sandbox.ebay.com/sell/inventory/v1/inventory_item"


def _read_json_file(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return None

    if isinstance(data, dict):
        return data

    return None


def _load_token() -> str | None:
    env_token = os.getenv("EBAY_SANDBOX_TOKEN", "").strip()
    if env_token:
        return env_token

    credentials = _read_json_file(CREDENTIALS_PATH)
    if not credentials:
        return None

    file_token = str(credentials.get("sandbox_token", "")).strip()
    if file_token:
        return file_token

    return None


def _write_result(result: dict[str, Any]) -> None:
    with RESULT_PATH.open("w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


def _blocked_result(status: str, reason: str) -> dict[str, Any]:
    return {
        "status": status,
        "reason": reason,
        "http_status": None,
        "response_body": None,
        "request_sent": False,
    }


def main() -> int:
    payload = _read_json_file(PAYLOAD_PATH)
    if payload is None:
        result = _blocked_result(
            status="NOT_READY",
            reason=f"Payload file missing or invalid: {PAYLOAD_PATH.name}",
        )
        _write_result(result)
        print("STATUS: NOT_READY")
        print(f"REASON: {result['reason']}")
        print(f"RESULT_FILE: {RESULT_PATH.name}")
        return 0

    token = _load_token()
    if not token:
        result = _blocked_result(
            status="BLOCKED",
            reason="Missing sandbox token (env EBAY_SANDBOX_TOKEN or ebay_sandbox_credentials_v1.json)",
        )
        _write_result(result)
        print("STATUS: BLOCKED")
        print(f"REASON: {result['reason']}")
        print(f"RESULT_FILE: {RESULT_PATH.name}")
        return 0

    inventory_url = str(payload.get("endpoint", DEFAULT_SANDBOX_URL)).strip() or DEFAULT_SANDBOX_URL

    try:
        timeout_seconds = int(payload.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
    except (TypeError, ValueError):
        timeout_seconds = DEFAULT_TIMEOUT_SECONDS

    body = payload.get("body")
    if not isinstance(body, dict):
        result = _blocked_result(
            status="NOT_READY",
            reason="Payload 'body' is missing or invalid",
        )
        _write_result(result)
        print("STATUS: NOT_READY")
        print(f"REASON: {result['reason']}")
        print(f"RESULT_FILE: {RESULT_PATH.name}")
        return 0

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.put(
            inventory_url,
            headers=headers,
            json=body,
            timeout=timeout_seconds,
        )
        try:
            response_body: Any = response.json()
        except ValueError:
            response_body = response.text

        result = {
            "status": "SUCCESS" if response.ok else "FAILED",
            "reason": "Request completed",
            "http_status": response.status_code,
            "response_body": response_body,
            "request_sent": True,
        }
    except requests.RequestException as exc:
        result = {
            "status": "FAILED",
            "reason": f"Request exception: {exc}",
            "http_status": None,
            "response_body": None,
            "request_sent": False,
        }

    _write_result(result)
    print(f"STATUS: {result['status']}")
    print(f"HTTP_STATUS: {result['http_status']}")
    print(f"RESULT_FILE: {RESULT_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())