import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = [
    "run_generator_agent_v1.py",
    "run_generator_agent_v2.py",
    "run_generator_agent_v3.py",
    "run_generator_agent_v4.py",
    "run_generator_agent_v5.py",
    "run_build_next_product_input_v1.py",
    "run_merge_next_product_with_live_template_v1.py",
    "run_memory_bootstrap_v1.py",
    "run_memory_lookup_v1.py"
]

REQUIRED_PATHS = [
    "storage",
    "storage\\exports",
    "storage\\memory",
    "storage\\products",
    "storage\\templates"
]

files_ok = []
files_missing = []
paths_ok = []
paths_missing = []

for rel in REQUIRED_FILES:
    p = ROOT / rel
    if p.exists() and p.is_file():
        files_ok.append(rel)
    else:
        files_missing.append(rel)

for rel in REQUIRED_PATHS:
    p = ROOT / rel
    if p.exists():
        paths_ok.append(rel)
    else:
        paths_missing.append(rel)

next_step = "build_generator_execution_probe_v1" if generator_ready else "repair_generator_layer_prerequisites"

report = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "generator_layer_readiness_audit_completed",
    "generator_ready": generator_ready,
    "files_ok_count": len(files_ok),
    "files_missing_count": len(files_missing),
    "paths_ok_count": len(paths_ok),
    "paths_missing_count": len(paths_missing),
    "files_missing": files_missing,
    "paths_missing": paths_missing,
    "next_step": next_step
}

out = EXPORT_DIR / "generator_layer_readiness_audit_v1.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("GENERATOR_LAYER_READINESS_AUDIT_DONE")
print("generator_ready =", generator_ready)
print("files_missing_count =", len(files_missing))
print("paths_missing_count =", len(paths_missing))
print("report =", out)
