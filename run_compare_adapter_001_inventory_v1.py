import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "storage" / "exports"
LIVE_PATH = EXPORT_DIR / "adapter_001_live_inventory_fetch_v1.json"
PLAN_PATH = EXPORT_DIR / "adapter_001_live_revise_package_v1.json"
OUT_PATH = EXPORT_DIR / "adapter_001_compare_inventory_v1.json"
def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
def main():
    live = load_json(LIVE_PATH)
    plan = load_json(PLAN_PATH)
    live_resp = live.get("response", {})
    live_product = live_resp.get("product", {})
    live_title = live_product.get("title", "")
    live_aspects = live_product.get("aspects", {})
    planned_title = plan.get("title", "")
    planned_specifics = plan.get("specifics", {})
    result = {
        "status": "OK",
        "product_key": plan.get("product_key"),
        "sku": plan.get("sku"),
        "live_title": live_title,
        "planned_title": planned_title,
        "title_changed": live_title != planned_title,
        "live_aspects_count": len(live_aspects),
        "planned_specifics_count": len(planned_specifics),
        "revise_ready": True,
        "decision": "prepare_full_inventory_revise_if_title_or_aspects_need_update"
    }
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("COMPARE_INVENTORY_V1")
    print("status =", result["status"])
    print("product =", result["product_key"])
    print("title_changed =", result["title_changed"])
    print("live_aspects_count =", result["live_aspects_count"])
    print("planned_specifics_count =", result["planned_specifics_count"])
    print("revise_ready =", result["revise_ready"])
if __name__ == "__main__":
    main()
