import json
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

p = EXPORT / "generator_v4_stdout_v1.txt"
text = p.read_text(encoding="utf-8", errors="ignore") if p.exists() else "" 
stripped = text.strip()
lines = [x for x in text.splitlines() if x.strip()]

result = {
"status": "OK",
"decision": "raw_stdout_preview_inspected",
"stdout_exists": p.exists(),
"stdout_len": len(text),
"line_count": len(lines),
"first_line": lines[0] if len(lines) > 0 else "",
"last_line": lines[-1] if len(lines) > 0 else "",
"stdout_preview": stripped[:500],
"contains_title_word": "title" in stripped.lower(),
"contains_description_word": "description" in stripped.lower(),
"contains_price_word": "price" in stripped.lower(),
"next_step": "register_raw_generator_output_pattern_v1"
}

(EXPORT / "raw_stdout_preview_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
(ARCHIVE / "raw_stdout_preview_v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("RAW_STDOUT_PREVIEW_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("stdout_exists =", result["stdout_exists"])
print("stdout_len =", result["stdout_len"])
print("line_count =", result["line_count"])
print("first_line =", result["first_line"])
print("last_line =", result["last_line"])
print("contains_title_word =", result["contains_title_word"])
print("contains_description_word =", result["contains_description_word"])
print("contains_price_word =", result["contains_price_word"])
print("next_step =", result["next_step"])
