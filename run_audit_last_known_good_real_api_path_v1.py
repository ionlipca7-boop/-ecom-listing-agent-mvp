
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def safe_read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except:
        return ""

def detect_flags(name, text):
    low = (name + " " + text).lower()
    return {
        "inventory": "inventory" in low,
        "offer": "offer" in low,
        "publish": "publish" in low,
        "quantity": "quantity" in low,
        "token_auth": ("token" in low or "oauth" in low or "authorization" in low or "refresh" in low),
        "registry": ("registry" in low or "product_key" in low),
        "ebay": ("ebay" in low or "api.ebay.com" in low),
        "requests": ("import requests" in low or "requests." in low),
    }

def score(flags):
    s = 0
    if flags["ebay"]:
        s += 3
    if flags["requests"]:
        s += 2
    if flags["inventory"]:
        s += 2
    if flags["offer"]:
        s += 2
    if flags["publish"]:
        s += 2
    if flags["quantity"]:
        s += 2
    if flags["token_auth"]:
        s += 1
    if flags["registry"]:
        s += 1
    return s

def main():
    candidates = []

    for path in sorted(BASE_DIR.glob("run_*.py")):
        text = safe_read_text(path)
        flags = detect_flags(path.name, text)
        sc = score(flags)

        if sc > 0:
            candidates.append({
                "file": path.name,
                "score": sc,
                "flags": flags
            })

    candidates.sort(key=lambda x: (-x["score"], x["file"]))
    top = candidates[:10]

    inventory = [x["file"] for x in top if x["flags"]["inventory"]]
    offer = [x["file"] for x in top if x["flags"]["offer"]]
    publish = [x["file"] for x in top if x["flags"]["publish"]]
    quantity = [x["file"] for x in top if x["flags"]["quantity"]]
    token = [x["file"] for x in top if x["flags"]["token_auth"]]

    out = {
        "status": "OK",
        "decision": "last_known_good_real_api_path_v1_audited",
        "total": len(candidates),
        "best": top[0]["file"] if top else None,
        "inventory_files": inventory,
        "offer_files": offer,
        "publish_files": publish,
        "quantity_files": quantity,
        "token_files": token
    }

    (EXPORTS_DIR / "last_known_good_real_api_path_v1.json").write_text(
        json.dumps(out, indent=2),
        encoding="utf-8"
    )

    print("LAST_KNOWN_GOOD_REAL_API_PATH_V1_FINAL_AUDIT")
    print("status =", out["status"])
    print("decision =", out["decision"])
    print("total =", out["total"])
    print("best =", out["best"])
    print("inventory_files =", out["inventory_files"])
    print("offer_files =", out["offer_files"])
    print("publish_files =", out["publish_files"])
    print("quantity_files =", out["quantity_files"])
    print("token_files =", out["token_files"])

if __name__ == "__main__":
    main()
cd /d D:\ECOM_LISTING_AGENT_MVP && echo ===== CONTROL_ROOM_PROJECT_RECHECK_V1 ===== && echo. && echo [1] RECENT RUN FILES && dir /b /o-d run_*.py && echo. && echo [2] KNOWN WORKING FILE CHECK && if exist run_ebay_update_offer_v2.py (echo run_ebay_update_
