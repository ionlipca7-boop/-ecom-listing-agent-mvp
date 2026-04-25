import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ITEM_ID = "318166440509"
OUT = ROOT / "storage" / "memory" / "archive" / "live_listing_recovery_audit_v2.json"
TOKEN_CANDIDATES = [
    ROOT / "storage" / "secrets" / "ebay_access_token.txt",
    ROOT / "storage" / "secrets" / "ebay_refresh_token.txt",
    ROOT / "ebay_access_token.txt",
    ROOT / "ebay_refresh_token.txt",
]

def token_info(path):
    if not path.exists():
        return {"path": str(path.relative_to(ROOT)), "exists": False, "length": 0}
    text = path.read_text(encoding="utf-8").strip()
    return {"path": str(path.relative_to(ROOT)), "exists": True, "length": len(text), "starts_with": text[:12]}

def extract_values(text, key_name):
    values = []
    marker = chr(34) + key_name + chr(34) + ": " + chr(34)
    parts = text.split(marker)
    for part in parts[1:]:
        value = part.split(chr(34))[0]
        if value and value not in values:
            values.append(value)
    return values

def find_hits():
    hits = []
    offer_ids = []
    skus = []
    for path in ROOT.rglob("*.json"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if ITEM_ID not in text:
            continue
        rel = str(path.relative_to(ROOT))
        local_offer_ids = extract_values(text, "offerId")
        local_skus = extract_values(text, "sku")
        for x in local_offer_ids:
            if x not in offer_ids:
                offer_ids.append(x)
        for x in local_skus:
            if x not in skus:
                skus.append(x)
        hits.append({"path": rel, "offer_ids": local_offer_ids[:5], "skus": local_skus[:5]})
    return hits, offer_ids, skus

def main():
    tokens = [token_info(p) for p in TOKEN_CANDIDATES]
    hits, offer_ids, skus = find_hits()
    result = {}
    result["status"] = "OK"
    result["decision"] = "live_listing_recovery_audit_v2_completed"
    result["item_id"] = ITEM_ID
    result["tokens"] = tokens
    result["json_hits_count"] = len(hits)
    result["offer_id_candidates"] = offer_ids[:10]
    result["sku_candidates"] = skus[:10]
    result["sample_hits"] = hits[:10]
    result["next_step"] = "use_offer_candidate_for_live_offer_read_and_inventory_bridge_restore"
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("LIVE_LISTING_RECOVERY_AUDIT_V2")
    print("status =", result["status"])
    print("json_hits_count =", result["json_hits_count"])
    print("offer_id_candidates =", result["offer_id_candidates"])
    print("sku_candidates =", result["sku_candidates"])
if __name__ == "__main__":
    main()
