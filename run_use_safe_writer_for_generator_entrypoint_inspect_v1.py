import json
from pathlib import Path

ROOT = Path(".")
EXPORT_DIR = ROOT / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

target = ROOT / "run_generator_entrypoint_inspect_v1.py"
from pathlib import Path

ROOT = Path(".")
EXPORT_DIR = ROOT / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "run_generator_agent_v1.py",
    "run_generator_agent_v2.py",
    "run_generator_agent_v3.py",
    "run_generator_agent_v4.py",
    "run_generator_agent_v5.py"
]

rows = []
for name in FILES:
    p = ROOT / name
    if p.exists():
        text = p.read_text(encoding="utf-8", errors="ignore")
        row = {
            "file": name,
            "exists": True,
            "size": p.stat().st_size,
            "has_main_guard": "__main__" in text,
            "has_main_def": "def main(" in text,
            "has_print": "print(" in text,
            "has_json": "json" in text
        }
    else:
        row = {
            "file": name,
            "exists": False,
            "size": 0,
            "has_main_guard": False,
            "has_main_def": False,
            "has_print": False,
            "has_json": False
        }
    rows.append(row)

result = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "generator_entrypoint_inspected",
    "files": rows
}

out = EXPORT_DIR / "generator_entrypoint_inspect_v1.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("GENERATOR_ENTRYPOINT_INSPECT_DONE")
print("report =", out)
target.write_text(content, encoding="utf-8")

result = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "safe_writer_created_generator_entrypoint_inspect",
    "target_file": str(target),
    "target_exists": target.exists(),
    "target_size": target.stat().st_size if target.exists() else 0,
    "next_step": "run_generator_entrypoint_inspect_v1"
}

out = EXPORT_DIR / "safe_writer_generator_entrypoint_inspect_v1.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("SAFE_WRITER_GENERATOR_ENTRYPOINT_DONE")
print("target_exists =", target.exists())
print("report =", out)
