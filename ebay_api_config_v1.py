from pathlib import Path

CONFIG_TEMPLATE = """# eBay API local config
# Fill these values after eBay Developers approval.

EBAY_ENV = "SANDBOX"

# From Application Keys
EBAY_CLIENT_ID = "PASTE_CLIENT_ID_HERE"
EBAY_CLIENT_SECRET = "PASTE_CLIENT_SECRET_HERE"

# OAuth / user token
EBAY_REDIRECT_URI = "PASTE_RUNAME_HERE"
EBAY_ACCESS_TOKEN = "PASTE_SANDBOX_ACCESS_TOKEN_HERE"

# Inventory / offer defaults
EBAY_DEFAULT_MARKETPLACE_ID = "EBAY_DE"
EBAY_DEFAULT_CATEGORY_ID = "58058"
EBAY_DEFAULT_LOCATION_KEY = "main_de_location"
EBAY_DEFAULT_CURRENCY = "EUR"
EBAY_DEFAULT_COUNTRY = "DE"
"""

OUTPUT_FILE = Path("ebay_api_config_v1.py.txt")


def main():
    OUTPUT_FILE.write_text(CONFIG_TEMPLATE, encoding="utf-8")
    print("CONFIG TEMPLATE CREATED:")
    print(f"file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()