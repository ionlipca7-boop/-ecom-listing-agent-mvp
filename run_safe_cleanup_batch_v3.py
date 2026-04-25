import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "storage" / "exports"
QUARANTINE_ROOT = ROOT / "storage" / "cleanup" / "safe_cleanup_batch_v3"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_ROOT.mkdir(parents=True, exist_ok=True)

TARGET_NAME = "cleanup_backup"
src = ROOT / TARGET_NAME
dst = QUARANTINE_ROOT / TARGET_NAME

moved = False
not_found = False
failed = None

if not src.exists():
    not_found = True
else:
    try:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(src), str(dst))
        moved = True
    except Exception as e:
        failed = str(e)

report = {
    "status": "OK" if failed is None else "ERROR",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "safe_cleanup_batch_v3_executed",
    "target_name": TARGET_NAME,
    "source_exists_before": not not_found,
    "moved": moved,
    "not_found": not_found,
    "failed": failed,
    "quarantine_path": str(dst),
    "rule": "quarantine_cleanup_backup_only" 
}

out = EXPORT_DIR / "safe_cleanup_batch_v3_result.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("SAFE_CLEANUP_BATCH_V3_DONE")
print("status =", report["status"])
print("moved =", report["moved"])
print("not_found =", report["not_found"])
print("report =", out)
