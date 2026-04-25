import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
ROUTER_FILE = EXPORTS_DIR / "ebay_upload_result_router_v1.json"
MASTER_FILE = EXPORTS_DIR / "control_room_master_status_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "listing_performance_v1.json"

def read_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    router = read_json(ROUTER_FILE)
    master = read_json(MASTER_FILE)

    route_status = "MISSING"
    route_target = "MISSING"
    master_status = "MISSING"

    if router:
        route_status = router.get("route_status", "MISSING")
        route_target = router.get("route_target", "MISSING")

    if master:
        master_status = master.get("master_status", "MISSING")

    if route_status == "CONFIRMED":
        performance_status = "READY"
        stage = "BASELINE_TRACKING_OPENED"
        next_step = "COLLECT_REAL_MARKET_METRICS"
    elif route_status == "REVIEW":
        performance_status = "BLOCKED_BY_REVIEW"
        stage = "WAIT_REVIEW_RESULT"
        next_step = "RESOLVE_UPLOAD_WARNINGS_FIRST"
    elif route_status == "FIX_REQUIRED":
        performance_status = "BLOCKED_BY_ERRORS"
        stage = "WAIT_FIX_RESULT"
        next_step = "FIX_UPLOAD_ERRORS_FIRST"
    else:
        performance_status = "WAITING"
        stage = "NOT_READY"
        next_step = "CHECK_POST_UPLOAD_ROUTE"

    tracking_fields = dict(views=0, watchers=0, quantity_sold=0, returns=0, revenue=0)

    output = {
        "performance_status": performance_status,
        "stage": stage,
        "next_step": next_step,
        "summary": {
            "master_status": master_status,
            "route_status": route_status,
            "route_target": route_target
        },
        "tracking_fields": tracking_fields,
        "inputs": {
            "router_file": str(ROUTER_FILE),
            "master_file": str(MASTER_FILE)
        }
    }

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print("LISTING_PERFORMANCE_V1:")
    print("performance_status:", output["performance_status"])
    print("stage:", output["stage"])
    print("route_status:", output["summary"]["route_status"])
    print("next_step:", output["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
