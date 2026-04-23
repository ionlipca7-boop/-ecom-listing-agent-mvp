import json
from pathlib import Path
from typing import Any

CONFIG_FILE = Path("publish_mode_config_v1.json")
LOCATION_FILE = Path("ebay_location_payload_v1.json")
INVENTORY_FILE = Path("ebay_inventory_payload_v1.json")
OFFER_FILE = Path("ebay_offer_payload_v1.json")


def _safe_read_json(path: Path) -> tuple[bool, Any | None]:
    try:
        return True, json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return False, None
    except json.JSONDecodeError:
        return False, None


def _file_ok(path: Path) -> tuple[bool, str]:
    ok, data = _safe_read_json(path)
    if not ok:
        return False, "missing_or_invalid_json"
    if not isinstance(data, dict):
        return False, "not_object"
    if not data:
        return False, "empty_object"
    return True, "ok"


def main() -> None:
    config_ok, config_data = _safe_read_json(CONFIG_FILE)

    mode = "unknown"
    if config_ok and isinstance(config_data, dict):
        mode = str(config_data.get("mode", "unknown")).strip().lower()

    checks = {
        "publish_mode_config_v1.json": {
            "exists": CONFIG_FILE.exists(),
            "valid_json": config_ok and isinstance(config_data, dict),
            "mode": mode,
        }
    }

    location_ok, location_reason = _file_ok(LOCATION_FILE)
    inventory_ok, inventory_reason = _file_ok(INVENTORY_FILE)
    offer_ok, offer_reason = _file_ok(OFFER_FILE)

    checks["ebay_location_payload_v1.json"] = {
        "exists": LOCATION_FILE.exists(),
        "status": location_reason,
    }
    checks["ebay_inventory_payload_v1.json"] = {
        "exists": INVENTORY_FILE.exists(),
        "status": inventory_reason,
    }
    checks["ebay_offer_payload_v1.json"] = {
        "exists": OFFER_FILE.exists(),
        "status": offer_reason,
    }

    ready = (
        mode == "sandbox"
        and location_ok
        and inventory_ok
        and offer_ok
    )

    print("EBAY SANDBOX READINESS V1:")
    print(f"mode: {mode}")
    print(f"location_payload: {location_reason}")
    print(f"inventory_payload: {inventory_reason}")
    print(f"offer_payload: {offer_reason}")
    print(f"status: {'READY' if ready else 'NOT_READY'}")

    if not ready:
        print("next_step: PREPARE_SANDBOX_MODE_OR_MISSING_PAYLOADS")
    else:
        print("next_step: SAFE_TO_ROUTE_TO_SANDBOX")


if __name__ == "__main__":
    main()