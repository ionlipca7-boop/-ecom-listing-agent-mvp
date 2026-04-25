import subprocess
import sys

from publish_mode_config_v1 import get_publish_mode


MODE_MAP = {
    "mock": "MOCK",
    "sandbox": "SANDBOX",
    "real": "PRODUCTION",
}


def run(cmd: str) -> None:
    print(f"\nRUNNING: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR: {cmd}")
        sys.exit(1)


def main() -> None:
    raw_mode = get_publish_mode()
    mode = MODE_MAP.get(raw_mode, "MOCK")

    print(f"PUBLISH ROUTER MODE: {mode}")
    print(f"PUBLISH ROUTER SOURCE MODE: {raw_mode}")

    if mode == "MOCK":
        run("python ebay_publish_executor_mock_v1.py")

    elif mode == "SANDBOX":
        run("python ebay_api_executor_inventory_v1.py")

    elif mode == "PRODUCTION":
        run("python ebay_api_executor_real_v1.py")

    else:
        print("ERROR: UNKNOWN MODE")
        sys.exit(1)


if __name__ == "__main__":
    main()