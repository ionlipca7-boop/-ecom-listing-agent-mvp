import json
from pathlib import Path

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

sel = json.loads((EXPORT / "generator_main_entrypoint_selection_v1.json").read_text(encoding="utf-8"))
selected = sel["selected_file"]
p = ROOT / selected
text = p.read_text(encoding="utf-8", errors="ignore")
low = text.lower()

result = {
"status": "OK",
"decision": "selected_generator_io_contract_inspected",
"selected_file": selected,
"has_main_def": "def main(" in text,
"has_main_guard": "__main__" in text,
"mentions_product": "product" in low,
"mentions_title": "title" in low,
"mentions_description": "description" in low,
"mentions_price": "price" in low,
"mentions_json_load": "json.load" in low or "json.loads" in low,
"mentions_json_dump": "json.dump" in low or "json.dumps" in low,
"mentions_read_text": "read_text(" in low,
"mentions_write_text": "write_text(" in low,
"mentions_print": "print(" in low,
"next_step": "build_generator_real_dry_input_v1"
}

(EXPORT / "selected_generator_io_contract_v1.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
(ARCHIVE / "selected_generator_io_contract_v1.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

print("SELECTED_GENERATOR_IO_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("selected_file =", result["selected_file"])
print("mentions_title =", result["mentions_title"])
print("mentions_description =", result["mentions_description"])
print("mentions_price =", result["mentions_price"])
print("mentions_json_load =", result["mentions_json_load"])
print("mentions_json_dump =", result["mentions_json_dump"])
print("next_step =", result["next_step"])
