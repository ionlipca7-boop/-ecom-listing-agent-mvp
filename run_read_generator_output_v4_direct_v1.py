import json
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

p = EXPORT / "generator_output_v4.json"
exists = p.exists()
parsed_ok = False
has_title = False
has_description = False
has_price = False
parse_error = "" 
preview = "" 

if exists:
    raw = p.read_text(encoding="utf-8", errors="ignore")
    preview = raw[:400]
    try:
        data = json.loads(raw)
        parsed_ok = True
        if isinstance(data, dict):
            has_title = "title" in data
            has_description = "description" in data
            has_price = "price" in data
    except Exception as e:
        parse_error = str(e)

result = {
"status": "OK",
"decision": "generator_output_v4_read_direct_completed",
"output_exists": exists,
"parsed_ok": parsed_ok,
"has_title": has_title,
"has_description": has_description,
"has_price": has_price,
"parse_error": parse_error,
"preview": preview,
"next_step": "promote_generator_v4_as_operational_entrypoint" if parsed_ok else "inspect_generator_output_v4_file_content_manually"
}

(EXPORT / "generator_output_v4_direct_read_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
(ARCHIVE / "generator_output_v4_direct_read_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("GENERATOR_OUTPUT_V4_DIRECT_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("output_exists =", result["output_exists"])
print("parsed_ok =", result["parsed_ok"])
print("has_title =", result["has_title"])
print("has_description =", result["has_description"])
print("has_price =", result["has_price"])
print("next_step =", result["next_step"])
