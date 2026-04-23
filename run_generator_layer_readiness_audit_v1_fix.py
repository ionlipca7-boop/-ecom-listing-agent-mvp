import json
from pathlib import Path

ROOT = Path(".")
EXPORT_DIR = ROOT / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    "run_generator_agent_v1.py",
    "run_generator_agent_v2.py",
    "run_generator_agent_v3.py",
    "run_generator_agent_v4.py",
    "run_generator_agent_v5.py"
]

REQUIRED_DIRS = [
    "storage",
    "storage\\exports",
    "storage\\memory",
    "storage\\products"
]

files_missing = []
dirs_missing = []

for name in REQUIRED_FILES:
    if not (ROOT / name).is_file():
        files_missing.append(name)

for name in REQUIRED_DIRS:
    if not (ROOT / name).exists():
        dirs_missing.append(name)

generator_ready = len(files_missing) == 0 and len(dirs_missing) == 0

if generator_ready:
    next_step = "build_generator_execution_probe_v1"
else:
    next_step = "repair_generator_prerequisites"

result = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "generator_layer_readiness_audit_fixed_completed",
    "generator_ready": generator_ready,
    "files_missing_count": len(files_missing),
    "dirs_missing_count": len(dirs_missing),
    "files_missing": files_missing,
    "dirs_missing": dirs_missing,
    "next_step": next_step
}

out = EXPORT_DIR / "generator_layer_readiness_audit_v1.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("GENERATOR_LAYER_READINESS_FIX_DONE")
print("generator_ready =", generator_ready)
print("files_missing_count =", len(files_missing))
print("dirs_missing_count =", len(dirs_missing))
print("report =", out)
