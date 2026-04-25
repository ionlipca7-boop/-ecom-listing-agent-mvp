import json
from pathlib import Path

root = Path(r"D:\ECOM_LISTING_AGENT_MVP")
baseline_path = root / "storage" / "exports" / "listing_clone_baseline_v1.json"
state_dir = root / "storage" / "state_control"
state_dir.mkdir(parents=True, exist_ok=True)

if not baseline_path.exists():
    result = {
        "status": "ERROR",
        "layer": "BUILD_NEW_LISTING_FROM_CLONE_BASELINE_V1",
        "reason": "listing_clone_baseline_v1_not_found",
        "baseline_path": str(baseline_path),
        "next_allowed_action": "restore_listing_clone_baseline_v1" 
    }
    (state_dir / "build_new_listing_from_clone_baseline_v1_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1)

data = json.loads(baseline_path.read_text(encoding="utf-8"))
source_listing = data.get("source_listing", {})
template = data.get("new_listing_template", {})
missing = []
if not source_listing.get("offerId"): missing.append("source_listing.offerId")
if not source_listing.get("listingId"): missing.append("source_listing.listingId")
if not source_listing.get("sku"): missing.append("source_listing.sku")
if not template: missing.append("new_listing_template")
if not data.get("next_allowed_action"): missing.append("next_allowed_action")

if missing:
    result = {
        "status": "ERROR",
        "layer": "BUILD_NEW_LISTING_FROM_CLONE_BASELINE_V1",
        "reason": "baseline_contract_incomplete",
        "baseline_path": str(baseline_path),
        "missing_keys": missing,
        "next_allowed_action": "repair_listing_clone_baseline_v1" 
    }
    (state_dir / "build_new_listing_from_clone_baseline_v1_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1)

next_layer = {
    "status": "OK",
    "layer": "NEW_LISTING_FROM_CLONE_BASELINE_V1",
    "input_layer": "LISTING_CLONE_BASELINE_V1",
    "baseline_path": str(baseline_path),
    "clone_mode": data.get("clone_mode"),
    "source_of_truth": data.get("source_of_truth"),
    "source_listing": source_listing,
    "new_listing_template": template,
    "known_limitations": data.get("known_limitations", {}),
    "payload_ready": True,
    "execution_blocked": True,
    "live_execution_allowed": False,
    "runner_publish_now": False,
    "title_selected": template.get("title"),
    "price_selected": template.get("price"),
    "next_allowed_action": "build_clone_runner_preview_v1" 
}

result = {
    "status": "OK",
    "layer": "BUILD_NEW_LISTING_FROM_CLONE_BASELINE_V1",
    "decision": "new_listing_from_clone_baseline_v1_built",
    "baseline_path": str(baseline_path),
    "offerId": source_listing.get("offerId"),
    "listingId": source_listing.get("listingId"),
    "sku": source_listing.get("sku"),
    "title_selected": template.get("title"),
    "price_selected": template.get("price"),
    "next_allowed_action": "build_clone_runner_preview_v1" 
}

(state_dir / "new_listing_from_clone_baseline_v1.json").write_text(json.dumps(next_layer, ensure_ascii=False, indent=2), encoding="utf-8")
(state_dir / "build_new_listing_from_clone_baseline_v1_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
