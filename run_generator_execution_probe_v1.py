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

files_ok = []
files_missing = []

for name in REQUIRED_FILES:
    if (ROOT / name).is_file():
        files_ok.append(name)
    else:
        files_missing.append(name)

probe_input = {
    "product_key": "probe_generator_001",
    "title_seed": "USB-C Ladekabel 2m 60W",
    "category_hint": "Kabel",
    "marketplace": "EBAY_DE",
    "mode": "probe_only"
}

if probe_ready:
    next_step = "inspect_generator_agents_and_select_real_entrypoint"
else:
    next_step = "repair_missing_generator_files"

result = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "generator_execution_probe_completed",
    "probe_ready": probe_ready,
    "files_ok_count": len(files_ok),
    "files_missing_count": len(files_missing),
    "files_ok": files_ok,
    "files_missing": files_missing,
    "probe_input": probe_input,
    "next_step": next_step
}

out = EXPORT_DIR / "generator_execution_probe_v1.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("GENERATOR_EXECUTION_PROBE_DONE")
print("probe_ready =", probe_ready)
print("files_ok_count =", len(files_ok))
print("files_missing_count =", len(files_missing))
print("report =", out)
