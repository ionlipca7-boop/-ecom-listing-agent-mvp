import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
CATEGORY_TREE_ID = "0"
CATEGORY_ID = "44932"
API_URL = f"https://api.ebay.com/commerce/taxonomy/v1/category_tree/{CATEGORY_TREE_ID}/get_item_aspects_for_category?category_id={CATEGORY_ID}"
OUTPUT_FILE = EXPORTS_DIR / "ebay_category_aspects_44932_v1.json"

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").strip()

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    token = read_text(SECRETS_DIR / "ebay_access_token.txt")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Accept-Language": "de-DE",
        "Content-Language": "de-DE",
    }

    response = requests.get(API_URL, headers=headers, timeout=60)
    data = response.json()

    result = {
        "http_status": response.status_code,
        "categoryId": CATEGORY_ID,
        "aspects_count": len(data.get("aspects", [])) if isinstance(data, dict) else 0,
        "produktart": None,
        "response_json": data,
    }

    if isinstance(data, dict):
        for aspect in data.get("aspects", []):
            name = ((aspect.get("localizedAspectName") or "") if isinstance(aspect, dict) else "")
            if name.strip().lower() == "produktart":
                result["produktart"] = aspect
                break

    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("GET_CATEGORY_ASPECTS_V1_DONE")
    print("http_status =", response.status_code)
    print("categoryId =", CATEGORY_ID)
    print("aspects_count =", result["aspects_count"])
    print("produktart_found =", result["produktart"] is not None)
    if result["produktart"] is not None:
        pa = result["produktart"]
        print("produktart_mode =", pa.get("aspectConstraint", {}).get("aspectMode"))
        print("produktart_required =", pa.get("aspectConstraint", {}).get("aspectRequired"))
        vals = pa.get("aspectValues", [])
        print("produktart_values_preview =", [v.get("localizedValue") for v in vals[:15]])

if __name__ == "__main__":
    main()
