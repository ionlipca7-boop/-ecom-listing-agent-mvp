import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "first_real_multi_listing_input_stub_v1.json"
OUT_PATH = BASE_DIR / "storage" / "exports" / "first_real_multi_listing_input_filled_v1.json"

def main():
    if not SOURCE_PATH.exists():
        print("ERROR: SOURCE NOT FOUND")
        return

    data = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    stub = data.get("input_stub", {})

    stub["new_registry_key"] = "adapter_001"
    stub["new_sku"] = "USB-C-OTG-Adapter-6A-120W-q10-p4.49"
    stub["target_title"] = "USB-C OTG Adapter USB 3.0 Typ C auf USB-A 6A 120W Datenadapter"
    stub["target_price"] = "4.49"
    stub["category_id"] = "30363"
    stub["merchant_location_key"] = "ECOM_DE_LOC_1"
    stub["fulfillment_policy_id"] = "REPLACE_WITH_REAL"
    stub["payment_policy_id"] = "REPLACE_WITH_REAL"
    stub["return_policy_id"] = "REPLACE_WITH_REAL"

    result = {"status":"OK","decision":"filled","input":stub}

    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("FILL_OK")
    print("file_created =", OUT_PATH.exists())

if __name__ == "__main__":
    main()
