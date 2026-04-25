import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "auto_fix_error_map_v2.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "fix_execution_plan_v1.json"

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

def field_action(field_name):
    mapping = {}
    mapping["brand"] = {"target_field": "Brand", "repair_action": "fill_required_aspect", "source_layer": "template_or_item_specifics", "instruction": "Заполнить обязательный аспект Brand допустимым значением для категории."}
    mapping["item_specifics"] = {"target_field": "ItemSpecifics", "repair_action": "repair_item_specifics", "source_layer": "template_mapper", "instruction": "Проверить и дополнить обязательные item specifics по шаблону eBay."}
    mapping["price"] = {"target_field": "StartPrice", "repair_action": "normalize_price", "source_layer": "price_optimizer", "instruction": "Проверить формат цены и пересчитать цену в допустимом формате eBay."}
    mapping["title"] = {"target_field": "Title", "repair_action": "rebuild_title", "source_layer": "ai_title_optimizer", "instruction": "Пересобрать title с учетом SEO-формулы и лимита eBay."}
    mapping["description"] = {"target_field": "Description", "repair_action": "rebuild_description", "source_layer": "generator", "instruction": "Пересобрать description и убрать конфликтующие формулировки."}
    mapping["image"] = {"target_field": "PictureURL", "repair_action": "repair_images", "source_layer": "photo_manifest", "instruction": "Проверить наличие и корректность изображений в package assets."}
    mapping["shipping"] = {"target_field": "Shipping", "repair_action": "repair_shipping", "source_layer": "template_mapper", "instruction": "Проверить shipping fields и business policy values."}
    mapping["payment_policy"] = {"target_field": "PaymentPolicy", "repair_action": "repair_payment_policy", "source_layer": "business_policy", "instruction": "Проверить payment policy и допустимые значения."}
    mapping["return_policy"] = {"target_field": "ReturnPolicy", "repair_action": "repair_return_policy", "source_layer": "business_policy", "instruction": "Проверить return policy и допустимые значения."}
    mapping["business_policy"] = {"target_field": "BusinessPolicy", "repair_action": "repair_business_policy", "source_layer": "business_policy", "instruction": "Проверить business policy configuration перед повторной загрузкой."}
    mapping["unknown"] = {"target_field": "unknown", "repair_action": "manual_review", "source_layer": "operator", "instruction": "Нужен ручной разбор ошибки и добавление нового правила."}
    return mapping.get(field_name, mapping["unknown"])

def build_plan_for_issue(issue):
    probable_fields = issue.get("probable_fields") or []
    if not probable_fields:
        probable_field = issue.get("probable_field") or "unknown"
        probable_fields = [probable_field]
    actions = []
    step_index = int("1")
    for field_name in probable_fields:
        action = field_action(field_name)
        action_record = {}
        action_record["step_id"] = issue.get("issue_id", "ISSUE") + "_STEP_" + str(step_index)
        action_record["target_field"] = action["target_field"]
        action_record["repair_action"] = action["repair_action"]
        action_record["source_layer"] = action["source_layer"]
        action_record["instruction"] = action["instruction"]
        action_record["automation_ready"] = "YES" if action["repair_action"] != "manual_review" else "NO"
        actions.append(action_record)
        step_index = step_index + int("1")
    return actions

def main():
    ok, data, error = safe_read_json(INPUT_FILE)
    result = {}
    zero = int("0")
    result["generated_at"] = utc_now()
    result["source_file"] = str(INPUT_FILE)
    result["output_file"] = str(OUTPUT_FILE)
    result["plan_status"] = "READY"
    result["issues_count"] = zero
    result["action_count"] = zero
    result["plans"] = []
    if not ok:
        result["plan_status"] = "ERROR"
        result["error"] = error
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print("FIX_EXECUTION_PLAN_V1:")
        print("plan_status:", result["plan_status"])
        print("error:", error)
        print("output_file:", OUTPUT_FILE.name)
        return
    issues = data.get("issues", [])
    result["issues_count"] = len(issues)
    total_actions = zero
    for issue in issues:
        plan = {}
        plan["issue_id"] = issue.get("issue_id")
        plan["issue_type"] = issue.get("issue_type")
        plan["severity"] = issue.get("severity")
        plan["source_code"] = issue.get("source_code")
        plan["probable_fields"] = issue.get("probable_fields") or [issue.get("probable_field", "unknown")]
        plan["repair_actions"] = build_plan_for_issue(issue)
        total_actions = total_actions + len(plan["repair_actions"])
        result["plans"].append(plan)
    result["action_count"] = total_actions
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("FIX_EXECUTION_PLAN_V1:")
    print("plan_status:", result["plan_status"])
    print("issues_count:", result["issues_count"])
    print("action_count:", result["action_count"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
