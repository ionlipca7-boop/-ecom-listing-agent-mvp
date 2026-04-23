import json
from pathlib import Path
from typing import Any

CONFIG_FILE = Path("publish_mode_config_v1.json")
DEFAULT_MODE = "mock"
ALLOWED_MODES = {"mock", "sandbox", "real"}


def _safe_read_json(path: Path) -> tuple[bool, Any | None]:
    try:
        return True, json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False, None
    except json.JSONDecodeError:
        return False, None


def get_publish_mode() -> str:
    ok, data = _safe_read_json(CONFIG_FILE)
    if not ok or not isinstance(data, dict):
        return DEFAULT_MODE

    mode = str(data.get("mode", DEFAULT_MODE)).strip().lower()
    if mode not in ALLOWED_MODES:
        return DEFAULT_MODE

    return mode


def main() -> None:
    config_exists = CONFIG_FILE.exists()
    mode = get_publish_mode()

    print("PUBLISH MODE CONFIG V1:")
    print(f"config_file: {CONFIG_FILE.name}")
    print(f"config_exists: {config_exists}")
    print(f"mode: {mode}")
    print(f"allowed_modes: {', '.join(sorted(ALLOWED_MODES))}")


if __name__ == "__main__":
    main()