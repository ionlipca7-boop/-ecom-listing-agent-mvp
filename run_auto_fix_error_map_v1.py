import json
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "storage" / "exports" / "ebay_upload_result_parsed_v1.json"
OUTPUT_FILE = BASE_DIR / "storage" / "exports" / "auto_fix_error_map_v1.json"

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

def detect_probable_field(text):
    t = text.lower()
    mapping = {
        "title": ["title", "titel"],
        "description": ["description", "beschreibung"],
        "price": ["price", "preis"],
        "category": ["category", "kategorie"],
        "item_specifics": ["item specific", "aspect", "specifics", "attribute"],
        "image": ["image", "photo", "picture", "bild"],
        "shipping": ["shipping", "versand", "delivery"],
        "payment_policy": ["payment"],
        "return_policy": ["return"],
        "business_policy": ["policy"],
        "sku": ["sku"],
        "ean_upc": ["ean", "upc", "gtin"],
    }
    for field_name, words in mapping.items():
        for word in words:
            if word in t:
                return field_name
    return "unknown"

def build_fix(issue_type, probable_field):
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
    if probable_field != "unknown" and issue_type in ("MISSING_REQUIRED_FIELD", "INVALID_VALUE"):
        probable_cause = probable_cause + "; вероятное поле: " + probable_field
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
        print("AUTO_FIX_ERROR_MAP_V1:")
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
        probable_field = detect_probable_field(text)
        probable_cause, recommended_fix, automation_level = build_fix(issue_type, probable_field)
        record = {}
        record["issue_id"] = "ISSUE_" + str(index)
        record["source_bucket"] = status or "UNKNOWN"
        record["source_code"] = code
        record["source_message"] = text or "NO_MESSAGE"
        record["issue_type"] = issue_type
        record["severity"] = status_to_severity(status)
        record["probable_field"] = probable_field
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
    print("AUTO_FIX_ERROR_MAP_V1:")
    print("status:", payload["status"])
    print("issues_found:", payload["issues_found"])
    print("source_parser_status:", payload["source_parser_status"])
    print("output_file:", OUTPUT_FILE.name)

if __name__ == "__main__":
    main()
