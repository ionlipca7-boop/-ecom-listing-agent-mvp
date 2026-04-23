import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"

def load_json(name):
    path = EXPORTS_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    base_call = load_json("real_inventory_read_call_v1.json")
    resolution_stub = load_json("live_identifier_resolution_result_stub_v1.json")

    identifier_type = resolution_stub.get("identifier_type")
    identifier_value = resolution_stub.get("identifier_value")

    if not identifier_type:
        identifier_type = "sku"

    if not identifier_value:
        identifier_value = "REPLACE_WITH_RESOLVED_LIVE_IDENTIFIER"

    output = dict(base_call)
    output["status"] = "OK"
    output["decision"] = "real_inventory_read_call_v2_built"
    output["identifier_source"] = "resolved_live_identifier"
    output["identifier_type"] = identifier_type
    output["identifier_value"] = identifier_value
    output["ready_for_real_inventory_read"] = identifier_value != "REPLACE_WITH_RESOLVED_LIVE_IDENTIFIER"
    output["next_step"] = "perform_real_inventory_read_v1"

    out_path = EXPORTS_DIR / "real_inventory_read_call_v2.json"
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("REAL_INVENTORY_READ_CALL_V2_OK")
    print("identifier_type =", output["identifier_type"])
    print("identifier_value =", output["identifier_value"])
    print("ready_for_real_inventory_read =", output["ready_for_real_inventory_read"])

if __name__ == "__main__":
    main()
