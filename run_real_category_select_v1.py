import json
from pathlib import Path
import requests
import urllib.parse

BASE_DIR = Path(__file__).resolve().parent
SECRETS_DIR = BASE_DIR / "storage" / "secrets"
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_PATH = EXPORTS_DIR / "real_offer_request_payload_v2.json"
OUTPUT_PATH = EXPORTS_DIR / "real_category_select_v1.json"

def main():
    token = (SECRETS_DIR / "ebay_access_token.txt").read_text(encoding="utf-8").strip()
    payload_doc = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    payload = payload_doc.get("payload", {})
    query = payload_doc.get("sku", "")
    if not query:
        query = payload.get("sku", "")
    if not query:
        query = "USB-C Ladekabel 2m 60W Schnellladen Datenkabel"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_DE"
    }

    tree_url = "https://api.ebay.com/commerce/taxonomy/v1/get_default_category_tree_id?marketplace_id=EBAY_DE"
    tree_resp = requests.get(tree_url, headers=headers, timeout=60)
    tree_data = tree_resp.json()
    tree_id = tree_data.get("categoryTreeId", "")

    encoded_q = urllib.parse.quote(query)
    suggest_url = "https://api.ebay.com/commerce/taxonomy/v1/category_tree/" + str(tree_id) + "/get_category_suggestions?q=" + encoded_q
    suggest_resp = requests.get(suggest_url, headers=headers, timeout=60)
    try:
        suggest_data = suggest_resp.json()
    except Exception:
        suggest_data = {"raw_text": suggest_resp.text[:2000]}

    suggestions = []
    for item in suggest_data.get("categorySuggestions", []):
        cat = item.get("category", {})
        suggestions.append({
            "categoryId": cat.get("categoryId", ""),
            "categoryName": cat.get("categoryName", ""),
            "categoryTreeNodeLevel": item.get("categoryTreeNodeLevel"),
            "categorySubtreeNodeHref": item.get("categorySubtreeNodeHref", "")
        })

    best = suggestions[0] if suggestions else {}
    result = {
        "status": "OK" if tree_resp.status_code == 200 and suggest_resp.status_code == 200 else "FAILED",
        "decision": "category_selected" if best.get("categoryId") else "no_category_found",
        "query": query,
        "category_tree_id": tree_id,
        "http_statuses": {
            "default_tree": tree_resp.status_code,
            "suggestions": suggest_resp.status_code
        },
        "selected_category": best,
        "suggestions": suggestions[:10]
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("REAL_CATEGORY_SELECT_V1")
    print("default_tree_http =", tree_resp.status_code)
    print("suggestions_http =", suggest_resp.status_code)
    print("query =", query)
    print("selected_categoryId =", best.get("categoryId", ""))
    print("selected_categoryName =", best.get("categoryName", ""))

if __name__ == "__main__":
    main()
