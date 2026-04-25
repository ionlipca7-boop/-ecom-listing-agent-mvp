import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "storage" / "memory" / "archive" / "policy_recovery_audit_v1.json"

def extract_values(text, key_name):
    values = []
    marker = chr(34) + key_name + chr(34) + ": " + chr(34)
    parts = text.split(marker)
    for part in parts[1:]:
        value = part.split(chr(34))[0]
        if value and value not in values:
            values.append(value)
    return values

def main():
    hits = []
    fulfillment_ids = []
    payment_ids = []
    return_ids = []
    for path in ROOT.rglob("*.json"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        f_ids = extract_values(text, "fulfillmentPolicyId")
        p_ids = extract_values(text, "paymentPolicyId")
        r_ids = extract_values(text, "returnPolicyId")
        if f_ids or p_ids or r_ids:
            rel = str(path.relative_to(ROOT))
            hits.append({"path": rel, "fulfillmentPolicyIds": f_ids[:5], "paymentPolicyIds": p_ids[:5], "returnPolicyIds": r_ids[:5]})
        for x in f_ids:
            if x not in fulfillment_ids:
                fulfillment_ids.append(x)
        for x in p_ids:
            if x not in payment_ids:
                payment_ids.append(x)
        for x in r_ids:
            if x not in return_ids:
                return_ids.append(x)
    result = {}
    result["status"] = "OK"
    result["decision"] = "policy_recovery_audit_v1_completed"
    result["hits_count"] = len(hits)
    result["fulfillmentPolicyId_candidates"] = fulfillment_ids[:10]
    result["paymentPolicyId_candidates"] = payment_ids[:10]
    result["returnPolicyId_candidates"] = return_ids[:10]
    result["sample_hits"] = hits[:10]
    result["next_step"] = "build_full_offer_update_with_real_policy_ids_and_shipping_rules"
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("POLICY_RECOVERY_AUDIT_V1")
    print("status =", result["status"])
    print("hits_count =", result["hits_count"])
    print("fulfillmentPolicyId_candidates =", result["fulfillmentPolicyId_candidates"])
    print("paymentPolicyId_candidates =", result["paymentPolicyId_candidates"])
    print("returnPolicyId_candidates =", result["returnPolicyId_candidates"])
if __name__ == "__main__":
    main()
