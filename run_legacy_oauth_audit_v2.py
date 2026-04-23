from pathlib import Path

ROOT = Path(r"D:\ECOM_LISTING_AGENT_MVP")
SECRETS = ROOT / "storage" / "secrets"

files = [
    "ebay_refresh_token.txt",
    "ebay_user_access_token.txt",
    "ebay_access_token.txt",
    "ebay_client_id.txt",
    "ebay_client_secret.txt",
    "ebay_redirect_uri.txt"
]

print("LEGACY_OAUTH_PATH_AUDIT")

for name in files:
    p = SECRETS / name
    exists = p.exists()

    if exists:
        size = p.stat().st_size
    else:
        size = 0

    print(name, "exists =", exists, "| size =", size)

print("next_step = check_refresh_token_presence")