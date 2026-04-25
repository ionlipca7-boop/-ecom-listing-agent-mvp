import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "storage" / "exports"
QUARANTINE_DIR = ROOT / "storage" / "cleanup" / "safe_cleanup_batch_v1"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

SAFE_FILE_SUFFIXES = {".pyc", ".log", ".tmp", ".bak", ".old", ".orig"}
SAFE_DIR_NAMES = {"__pycache__"}
PROTECTED_DIRS = {"core", "storage", "adapter_001", ".git", ".github", ".venv", "venv", "agent", "app", "publisher", "templates", "drafts", "logs", "tests", "configs"}

moved = []
skipped = []

for item in ROOT.iterdir():
    name = item.name
    if item.is_dir():
        if name in PROTECTED_DIRS:
            skipped.append({"name": name, "reason": "protected_dir"})
            continue
        if name in SAFE_DIR_NAMES:
            target = QUARANTINE_DIR / name
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(item), str(target))
            moved.append({"name": name, "type": "dir"})
        else:
            skipped.append({"name": name, "reason": "non_safe_dir"})
    elif item.is_file():
        if item.suffix.lower() in SAFE_FILE_SUFFIXES:
            target = QUARANTINE_DIR / name
            if target.exists():
                target.unlink()
            shutil.move(str(item), str(target))
            moved.append({"name": name, "type": "file"})
        else:
            skipped.append({"name": name, "reason": "protected_or_non_safe_file"})

report = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "safe_cleanup_batch_v1_executed",
    "root_path": str(ROOT),
    "quarantine_path": str(QUARANTINE_DIR),
    "moved_count": len(moved),
    "skipped_count": len(skipped),
    "moved": moved,
    "skipped_sample": skipped[:30],
    "rules": [
        "do_not_touch_core",
        "do_not_touch_storage",
        "do_not_touch_active_adapter_001",
        "move_only_safe_artifacts",
        "no_hard_delete" 
    ]
}

out = EXPORT_DIR / "safe_cleanup_batch_result_v1.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("SAFE_CLEANUP_BATCH_V1_DONE")
print("moved_count =", len(moved))
print("skipped_count =", len(skipped))
print("report =", out)
