import json
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

stdout_file = EXPORT / "generator_v4_stdout_v1.txt"
output_file = EXPORT / "generator_output_v4.json"
stdout_text = stdout_file.read_text(encoding="utf-8", errors="ignore") if stdout_file.exists() else "" 

output_exists = output_file.exists()
parsed_ok = False
has_title = False
has_description = False
has_price = False
parse_error = "" 

if output_exists:
    try:
        data = json.loads(output_file.read_text(encoding="utf-8"))
        parsed_ok = True
        if isinstance(data, dict):
            has_title = "title" in data
            has_description = "description" in data
            has_price = "price" in data
    except Exception as e:
        parse_error = str(e)

result = {
"status": "OK",
"decision": "raw_generator_output_pattern_registered",
"stdout_pattern": "status_plus_output_file_path",
"stdout_has_ok_marker": "GENERATOR_AGENT_V4_OK" in stdout_text,
"output_file_exists": output_exists,
"output_file_size": output_len,
"output_parsed_ok": parsed_ok,
"output_has_title": has_title,
"output_has_description": has_description,
"output_has_price": has_price,
"parse_error": parse_error,
"next_step": "promote_generator_v4_as_operational_entrypoint" if parsed_ok else "inspect_generator_output_file_raw_v1"
}

(EXPORT / "generator_output_pattern_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
(ARCHIVE / "generator_output_pattern_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("GENERATOR_OUTPUT_PATTERN_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("stdout_has_ok_marker =", result["stdout_has_ok_marker"])
print("output_file_exists =", result["output_file_exists"])
print("output_parsed_ok =", result["output_parsed_ok"])
print("output_has_title =", result["output_has_title"])
print("output_has_description =", result["output_has_description"])
print("output_has_price =", result["output_has_price"])
print("next_step =", result["next_step"])
