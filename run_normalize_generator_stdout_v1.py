import json
import ast
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

stdout_file = EXPORT / "generator_v4_stdout_v1.txt"
text = stdout_file.read_text(encoding="utf-8", errors="ignore") if stdout_file.exists() else "" 
stripped = text.strip()

normalized = None
parsed_ok = False
parse_method = "none"
parse_error = "" 
has_title = False
has_description = False
has_price = False

try:
    normalized = json.loads(stripped)
    parsed_ok = True
    parse_method = "json"
except Exception as e:
    parse_error = str(e)

if not parsed_ok:
    try:
        normalized = ast.literal_eval(stripped)
        parsed_ok = True
        parse_method = "literal_eval"
        parse_error = "" 
    except Exception as e:
        parse_error = str(e)

normalized_type = type(normalized).__name__ if normalized is not None else "none"

if isinstance(normalized, dict):
    has_title = "title" in normalized
    has_description = "description" in normalized
    has_price = "price" in normalized

result = {
"status": "OK",
"decision": "generator_stdout_normalized",
"stdout_exists": stdout_file.exists(),
"stdout_len": len(text),
"parsed_ok": parsed_ok,
"parse_method": parse_method,
"normalized_type": normalized_type,
"has_title": has_title,
"has_description": has_description,
"has_price": has_price,
"parse_error": parse_error,
"stdout_preview": stripped[:300],
"normalized_data": normalized if isinstance(normalized, (dict, list, str, int, float, bool)) or normalized is None else str(normalized),
"next_step": "register_generator_output_contract_v1" if parsed_ok else "inspect_raw_stdout_preview_v1"
}

(EXPORT / "generator_stdout_normalized_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
(ARCHIVE / "generator_stdout_normalized_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("GENERATOR_STDOUT_NORMALIZE_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("parsed_ok =", result["parsed_ok"])
print("parse_method =", result["parse_method"])
print("normalized_type =", result["normalized_type"])
print("has_title =", result["has_title"])
print("has_description =", result["has_description"])
print("has_price =", result["has_price"])
print("next_step =", result["next_step"])
