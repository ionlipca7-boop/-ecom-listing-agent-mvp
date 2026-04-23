import json
import os
from pathlib import Path
from typing import Any

CREDENTIALS_FILE = Path("ebay_sandbox_credentials_v1.json")
PLACEHOLDER_VALUES = {
    "",
    "YOUR_SANDBOX_TOKEN_HERE",
    "PASTE_TOKEN_HERE",
    "CHANGE_ME",
}


def _safe_read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return None

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None

    if isinstance(data, dict):
        return data

    return None


def _normalize_token(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _classify_token(token: str) -> str:
    if not token:
        return "TOKEN_MISSING"
    if token in PLACEHOLDER_VALUES:
        return "TOKEN_PLACEHOLDER"
    return "TOKEN_READY"


def main() -> int:
    env_token = _normalize_token(os.getenv("EBAY_SANDBOX_TOKEN"))
    file_data = _safe_read_json(CREDENTIALS_FILE)
    file_token = _normalize_token(file_data.get("sandbox_token")) if file_data else ""

    source = "none"
    token = ""

    if env_token:
        source = "env"
        token = env_token
    elif file_token or CREDENTIALS_FILE.exists():
        source = "file"
        token = file_token

    status = _classify_token(token)

    print("EBAY TOKEN STATUS V1:")
    print(f"credentials_file: {CREDENTIALS_FILE.name}")
    print(f"credentials_file_exists: {CREDENTIALS_FILE.exists()}")
    print(f"token_source: {source}")
    print(f"token_present: {bool(token)}")
    print(f"status: {status}")

    if status == "TOKEN_READY":
        print("next_step: SAFE_TO_RUN_SANDBOX_WITH_TOKEN")
    elif status == "TOKEN_PLACEHOLDER":
        print("next_step: REPLACE_PLACEHOLDER_WITH_REAL_TOKEN")
    else:
        print("next_step: WAIT_FOR_EBAY_APPROVAL_OR_ADD_TOKEN")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())