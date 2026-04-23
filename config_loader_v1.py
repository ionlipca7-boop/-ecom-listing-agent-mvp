from pathlib import Path

CONFIG_FILE = Path("ebay_api_config_v1.py.txt")


def load_config():
    config = {}

    if not CONFIG_FILE.exists():
        print("ERROR: config file not found")
        return config

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"')

                config[key] = value

    return config


def main():
    cfg = load_config()

    print("CONFIG LOADER:")
    for k, v in cfg.items():
        print(f"{k} = {v}")


if __name__ == "__main__":
    main()