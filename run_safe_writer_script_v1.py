import json
from pathlib import Path

ROOT = Path(".")
EXPORT_DIR = ROOT / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

target = ROOT / "safe_writer_probe_v1.py"
content = "print('SAFE_WRITER_PROBE_OK')\n"
target.write_text(content, encoding="utf-8")

result = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "safe_writer_script_built",
    "target_file": str(target),
    "target_exists": target.exists(),
    "target_size": target.stat().st_size if target.exists() else 0,
    "next_step": "use_safe_writer_for_generator_entrypoint_inspect"
}

out = EXPORT_DIR / "safe_writer_script_v1.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print("SAFE_WRITER_SCRIPT_DONE")
print("target_exists =", target.exists())
print("report =", out)
