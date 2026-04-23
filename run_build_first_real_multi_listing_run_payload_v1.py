import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "first_real_multi_listing_input_filled_v1.json"
OUT_PATH = BASE_DIR / "storage" / "exports" / "first_real_multi_listing_run_payload_v1.json"

def main():
    data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    inp = data.get("input", {})

    payload = {
        "status": "OK",
        "decision": "first_real_multi_listing_run_payload_v1_built",
        "mode": "baseline_clone",
        "runtime_ready_for_live": False,
        "blocking_fields": [],
        "inventory_payload": {
            "sku": inp.get("new_sku"),
            "title": inp.get("target_title"),
            "image_count_expected": 9,
            "merchant_location_key": inp.get("merchant_location_key"),
            "category_id": inp.get("category_id")
        },
        "offer_payload": {
            "price": inp.get("target_price"),
            "fulfillment_policy_id": inp.get("fulfillment_policy_id"),
            "payment_policy_id": inp.get("payment_policy_id"),
            "return_policy_id": inp.get("return_policy_id")
        },
        "next_step": "review_runtime_blockers_v1"
    }

    for k in ["fulfillment_policy_id","payment_policy_id","return_policy_id"]:
        v = inp.get(k, "")
        if not v or v == "REPLACE_WITH_REAL":
            payload["blocking_fields"].append(k)


    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("FIRST_REAL_MULTI_LISTING_RUN_PAYLOAD_V1_AUDIT")
    print("status = OK")
    print("decision = first_real_multi_listing_run_payload_v1_built")
    print("mode = baseline_clone")
    print("runtime_ready_for_live =", payload["runtime_ready_for_live"])
    print("blocking_fields_count =", len(payload["blocking_fields"]))
    print("next_step =", payload["next_step"])

if __name__ == "__main__":
    main()
