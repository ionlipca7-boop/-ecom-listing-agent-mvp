import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "real_fix_executor_v1.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "apply_fix_payload_v1.json"

def utc_now():
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

def safe_read_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return True, data, None
    except FileNotFoundError:
        return False, None, "input file not found: " + str(path)
    except json.JSONDecodeError as exc:
        return False, None, "invalid json: " + str(exc)
    except Exception as exc:
        return False, None, "unexpected read error: " + str(exc)

def build_patch_value(action_name, target_field):
    if action_name == "fill_required_aspect" and target_field == "Brand":
        return "REQUIRED_BRAND_VALUE_FROM_CATEGORY"
    if action_name == "repair_item_specifics" and target_field == "ItemSpecifics":
        return {"mode": "MERGE_REQUIRED_ASPECTS", "source": "CATEGORY_TEMPLATE"}
    if action_name == "normalize_price" and target_field == "StartPrice":
        return {"mode": "RECALCULATE_AND_NORMALIZE", "source": "PRICE_OPTIMIZER"}
    if action_name == "rebuild_title" and target_field == "Title":
        return {"mode": "REBUILD_TITLE", "source": "AI_TITLE_OPTIMIZER"}
    if action_name == "rebuild_description" and target_field == "Description":
        return {"mode": "REBUILD_DESCRIPTION", "source": "GENERATOR"}
    if action_name == "repair_images" and target_field == "PictureURL":
        return {"mode": "REATTACH_IMAGES", "source": "PHOTO_MANIFEST"}
    if action_name == "repair_shipping" and target_field == "Shipping":
        return {"mode": "NORMALIZE_SHIPPING", "source": "TEMPLATE_MAPPER"}
    return {"mode": "MANUAL_OR_FUTURE_HANDLER", "source": "CONTROL_ROOM"}

def main():
    ok, data, error = safe_read_json(INPUT_FILE)
    result = {}
    zero = int("0")
    one = int("1")
    result["generated_at"] = utc_now()
    result["source_file"] = str(INPUT_FILE)
    result["output_file"] = str(OUTPUT_FILE)
    result["payload_status"] = "READY"
    result["queue_items"] = zero
    result["patch_count"] = zero
    result["patches"] = []
    result["next_step"] = "REVIEW_AND_APPLY_PATCHES"
    if not ok:
        result["payload_status"] = "ERROR"
        result["error"] = error
        result["next_step"] = "FIX_REAL_FIX_EXECUTOR_INPUT"
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("APPLY_FIX_PAYLOAD_V1:")
        print("payload_status:", result["payload_status"])
        print("error:", error)
        print("output_file:", OUTPUT_FILE.name)
        return
    queue_items = data.get("queue", [])
    result["queue_items"] = len(queue_items)
    patch_count = zero
    for item in queue_items:
        if item.get("execution_status") != "QUEUED":
            continue
        patch = {}
        patch["patch_id"] = "PATCH_" + str(patch_count + one)
        patch["issue_id"] = item.get("issue_id")
        patch["step_id"] = item.get("step_id")
        patch["target_field"] = item.get("target_field")
        patch["repair_action"] = item.get("repair_action")
        patch["target_file"] = item.get("target_file")
        patch["instruction"] = item.get("instruction")
        patch["patch_value"] = build_patch_value(item.get("repair_action"), item.get("target_field"))
        patch["apply_mode"] = "PENDING_REVIEW"
        result["patches"].append(patch)
        patch_count = patch_count + one
    result["patch_count"] = patch_count
    if patch_count == zero:
        result["payload_status"] = "NO_PATCHES"
        result["next_step"] = "REVIEW_EXECUTOR_QUEUE"
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("APPLY_FIX_PAYLOAD_V1:")
    print("payload_status:", result["payload_status"])
    print("queue_items:", result["queue_items"])
    print("patch_count:", result["patch_count"])
    print("next_step:", result["next_step"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
