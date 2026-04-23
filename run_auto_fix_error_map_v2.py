import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "ebay_upload_result_parsed_v1.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "auto_fix_error_map_v2.json"

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

def as_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    try:
        return json.dumps(value, ensure_ascii=False)
    except Exception:
        return str(value)

def detect_issue_type(text):
    t = text.lower()
    if any(word in t for word in ["missing", "required", "pflicht", "mandatory", "not specified"]):
        return "MISSING_REQUIRED_FIELD"
    if any(word in t for word in ["invalid", "not valid", "ungültig", "format", "allowed value"]):
        return "INVALID_VALUE"
    if any(word in t for word in ["category", "kategorie", "aspect", "item specific"]):
        return "CATEGORY_OR_ASPECT_MISMATCH"
    if any(word in t for word in ["title", "titel"]):
        return "TITLE_ISSUE"
    if any(word in t for word in ["description", "beschreibung"]):
        return "DESCRIPTION_ISSUE"
    if any(word in t for word in ["price", "preis"]):
        return "PRICE_ISSUE"
    if any(word in t for word in ["image", "photo", "picture", "bild"]):
        return "IMAGE_ISSUE"
    if any(word in t for word in ["shipping", "versand", "delivery"]):
        return "SHIPPING_ISSUE"
    if any(word in t for word in ["policy", "return", "payment"]):
        return "POLICY_ISSUE"
    if any(word in t for word in ["duplicate", "already exists"]):
        return "DUPLICATE_LISTING"
    return "UNKNOWN_ISSUE"

def detect_probable_fields(text):
    t = text.lower()
    fields = []
    if "brand" in t:
        fields.append("brand")
    if "item specific" in t or "aspect" in t or "attribute" in t or "specifics" in t:
        fields.append("item_specifics")
    if "price" in t or "preis" in t:
        fields.append("price")
    if "title" in t or "titel" in t:
        fields.append("title")
    if "description" in t or "beschreibung" in t:
        fields.append("description")
    if "image" in t or "photo" in t or "picture" in t or "bild" in t:
        fields.append("image")
    if "shipping" in t or "versand" in t or "delivery" in t:
        fields.append("shipping")
    if "payment" in t:
        fields.append("payment_policy")
    if "return" in t:
        fields.append("return_policy")
    if "policy" in t:
        fields.append("business_policy")
    unique_fields = []
    for field in fields:
        if field not in unique_fields:
            unique_fields.append(field)
    return unique_fields

def build_fix(issue_type, probable_fields):
    fixes = {
        "MISSING_REQUIRED_FIELD": ("обязательное поле отсутствует или пустое", "заполнить обязательное поле по шаблону eBay и прогнать повторную валидацию", "RULE_BASED"),
        "INVALID_VALUE": ("значение не соответствует допустимому формату или allowed values", "нормализовать значение под eBay template или allowed values категории", "RULE_BASED"),
        "CATEGORY_OR_ASPECT_MISMATCH": ("категория или item specifics не совпадают с требованиями категории", "проверить category mapping и required aspects", "RULE_BASED"),
        "TITLE_ISSUE": ("title не проходит ограничение или содержит неподходящие данные", "пересобрать title по SEO-формуле и лимиту eBay", "AI_ASSISTED"),
        "DESCRIPTION_ISSUE": ("description неполная или некорректная", "пересобрать description из generator layer", "AI_ASSISTED"),
        "PRICE_ISSUE": ("price отсутствует или некорректен", "пересчитать цену через price optimizer", "RULE_BASED"),
        "IMAGE_ISSUE": ("изображения отсутствуют или прикреплены некорректно", "проверить photo manifest и package assets", "MANUAL_OR_SCRIPTED"),
        "SHIPPING_ISSUE": ("ошибка в shipping policy или shipping fields", "проверить shipping mapping и business policy values", "RULE_BASED"),
        "POLICY_ISSUE": ("ошибка policy settings или business account configuration", "проверить payment, return и business policies", "MANUAL_REVIEW"),
        "DUPLICATE_LISTING": ("объявление уже существует или конфликтует с похожим listing", "проверить existing listing, SKU и relist strategy", "MANUAL_REVIEW"),
        "UNKNOWN_ISSUE": ("причина не распознана автоматически", "нужен ручной разбор текста ошибки и добавление нового правила", "REVIEW"),
    }
    probable_cause, recommended_fix, automation_level = fixes.get(issue_type, fixes["UNKNOWN_ISSUE"])
    if probable_fields and issue_type in ("MISSING_REQUIRED_FIELD", "INVALID_VALUE"):
        probable_cause = probable_cause + "; вероятные поля: " + ", ".join(probable_fields)
    return probable_cause, recommended_fix, automation_level

def status_to_severity(status):
    s = as_text(status).upper()
    if s == "ERROR":
        return "ERROR"
    if s == "WARNING":
        return "WARNING"
    return "INFO"

def main():
    ok, data, error = safe_read_json(INPUT_FILE)
    payload = {
        "generated_at": utc_now(),
        "source_file": str(INPUT_FILE),
        "output_file": str(OUTPUT_FILE),
        "status": "READY",
        "issues_found": 0,
        "summary": {},
        "issues": [],
    }
    if not ok:
        payload["status"] = "ERROR"
        payload["error"] = error
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("AUTO_FIX_ERROR_MAP_V2:")
        print("status: ERROR")
        print("error:", error)
        print("output_file:", OUTPUT_FILE.name)
        return
    items = data.get("items", [])
    records = []
    zero = int("0")
    one = int("1")
    for index, item in enumerate(items, start=1):
        status = as_text(item.get("status")).upper()
        raw = item.get("raw", {})
        text = item.get("combined_text") or raw.get("message") or raw
        code = raw.get("result_code") or raw.get("code") or "NO_CODE"
        text = as_text(text)
        code = as_text(code)
        if status == "SUCCESS":
            continue
        issue_type = detect_issue_type(text)
        probable_fields = detect_probable_fields(text)
        probable_cause, recommended_fix, automation_level = build_fix(issue_type, probable_fields)
        record = {}
        record["issue_id"] = "ISSUE_" + str(index)
        record["source_bucket"] = status or "UNKNOWN"
        record["source_code"] = code
        record["source_message"] = text or "NO_MESSAGE"
        record["issue_type"] = issue_type
        record["severity"] = status_to_severity(status)
        record["probable_field"] = probable_fields[0] if probable_fields else "unknown"
        record["probable_fields"] = probable_fields
        record["probable_cause"] = probable_cause
        record["recommended_fix"] = recommended_fix
        record["automation_level"] = automation_level
        records.append(record)
    severity_counts = {}
    issue_type_counts = {}
    for record in records:
        key1 = record["severity"]
        key2 = record["issue_type"]
        if key1 not in severity_counts:
            severity_counts[key1] = zero
        if key2 not in issue_type_counts:
            issue_type_counts[key2] = zero
        severity_counts[key1] = severity_counts[key1] + one
        issue_type_counts[key2] = issue_type_counts[key2] + one
    payload["issues_found"] = len(records)
    payload["issues"] = records
    payload["source_parser_status"] = data.get("parser_status")
    payload["source_latest_file"] = data.get("latest_file")
    payload["source_summary"] = data.get("summary", {})
    payload["summary"] = {}
    payload["summary"]["total_issues"] = len(records)
    payload["summary"]["severity_counts"] = severity_counts
    payload["summary"]["issue_type_counts"] = issue_type_counts
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("AUTO_FIX_ERROR_MAP_V2:")
    print("status:", payload["status"])
    print("issues_found:", payload["issues_found"])
    print("source_parser_status:", payload["source_parser_status"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
