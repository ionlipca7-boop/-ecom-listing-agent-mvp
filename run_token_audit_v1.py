from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SECRET_DIR = BASE_DIR / "storage" / "secrets"
def read_clean(path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip().lstrip("\ufeff")
def main():
    access_path = SECRET_DIR / "ebay_access_token.txt"
    refresh_path = SECRET_DIR / "ebay_refresh_token.txt"
    user_path = SECRET_DIR / "ebay_user_token.txt"
    access = read_clean(access_path)
    refresh = read_clean(refresh_path)
    user = read_clean(user_path)
    print("TOKEN_AUDIT_V1")
    print("access_exists =", access is not None)
    print("access_length =", len(access) if access else 0)
    print("access_starts_with =", repr((access or "")[:25]))
    print("refresh_exists =", refresh is not None)
    print("refresh_length =", len(refresh) if refresh else 0)
    print("user_exists =", user is not None)
    print("user_length =", len(user) if user else 0)
if __name__ == "__main__":
    main()
