import json
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

stdout_file = EXPORT / "generator_v4_stdout_v1.txt"
text = stdout_file.read_text(encoding="utf-8", errors="ignore") if stdout_file.exists() else "" 
stripped = text.strip()

parsed_ok = False
parsed_type = "none"
has_title = False
has_description = False
has_price = False
parse_error = "" 

try:
    data = json.loads(stripped)
    parsed_ok = True
    parsed_type = type(data).__name__
    if isinstance(data, dict):
        has_title = "title" in data
        has_description = "description" in data
        has_price = "price" in data
except Exception as e:
    parse_error = str(e)

result = {
"status": "OK",
"decision": "generator_output_contract_inspected",
"stdout_exists": stdout_file.exists(),
"stdout_len": len(text),
"parsed_ok": parsed_ok,
"parsed_type": parsed_type,
"has_title": has_title,
"has_description": has_description,
"has_price": has_price,
"parse_error": parse_error,
"stdout_preview": stripped[:300],
"next_step": "register_generator_output_contract_v1" if parsed_ok else "normalize_generator_stdout_v1"
}

(EXPORT / "generator_output_contract_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
(ARCHIVE / "generator_output_contract_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("GENERATOR_OUTPUT_CONTRACT_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("stdout_exists =", result["stdout_exists"])
print("stdout_len =", result["stdout_len"])
print("parsed_ok =", result["parsed_ok"])
print("parsed_type =", result["parsed_type"])
print("has_title =", result["has_title"])
print("has_description =", result["has_description"])
print("has_price =", result["has_price"])
print("next_step =", result["next_step"])
