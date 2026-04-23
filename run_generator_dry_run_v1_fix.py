import json
from pathlib import Path
import py_compile

ROOT = Path(".")
EXPORT = ROOT / "storage" / "exports"
ARCHIVE = ROOT / "storage" / "memory" / "archive"
EXPORT.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)

sel = json.loads((EXPORT / "generator_main_entrypoint_selection_v1.json").read_text(encoding="utf-8"))
selected = sel["selected_file"]
p = ROOT / selected

exists = p.exists()
text = p.read_text(encoding="utf-8", errors="ignore") if exists else "" 

compile_ok = False
compile_error = "" 

try:
    py_compile.compile(str(p), doraise=True)
    compile_ok = True
except Exception as e:
    compile_error = str(e)

has_main_guard = "__main__" in text
has_main_def = "def main(" in text

result = {
"status": "OK" if exists else "ATTENTION",
"decision": "generator_dry_run_built",
"selected_file": selected,
"exists": exists,
"compile_ok": compile_ok,
"has_main_guard": has_main_guard,
"has_main_def": has_main_def,
"next_step": "inspect_selected_generator_io_contract_v1" if compile_ok else "repair_generator"
}

(EXPORT / "generator_dry_run_v1.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
(ARCHIVE / "generator_dry_run_v1.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

print("GENERATOR_DRY_RUN_AUDIT")
print("status =", result["status"])
print("decision =", result["decision"])
print("selected_file =", result["selected_file"])
print("compile_ok =", result["compile_ok"])
print("next_step =", result["next_step"])
