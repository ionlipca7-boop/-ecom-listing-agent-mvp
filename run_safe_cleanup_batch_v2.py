import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "storage" / "exports"
QUARANTINE_DIR = ROOT / "storage" / "cleanup" / "safe_cleanup_batch_v2"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

SAFE_NAMES = [
    "cd",
    "chcp",
    "del",
    "dict",
    "echo",
    "list",
    "None",
    "python",
    "str",
    "type",
    "run_ebay_create_inventory_item_v3.pycd",
    "run_ebay_get_category_suggestions_v1.pypython",
    "run_ebay_publish_draft_v1.pycd"
]

moved = []
not_found = []
failed = []

for name in SAFE_NAMES:
    src = ROOT / name
    if not src.exists():
        not_found.append(name)
        continue
    dst = QUARANTINE_DIR / name
    try:
        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()
        shutil.move(str(src), str(dst))
        moved.append(name)
    except Exception as e:
        failed.append({"name": name, "error": str(e)})

report = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "safe_cleanup_batch_v2_executed",
    "quarantine_path": str(QUARANTINE_DIR),
    "safe_names_count": len(SAFE_NAMES),
    "moved_count": len(moved),
    "not_found_count": len(not_found),
    "failed_count": len(failed),
    "moved": moved,
    "not_found": not_found,
    "failed": failed,
    "rule": "delete_only_from_safe_list_first"
}

out = EXPORT_DIR / "safe_cleanup_batch_v2_result.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("SAFE_CLEANUP_BATCH_V2_DONE")
print("moved_count =", len(moved))
print("not_found_count =", len(not_found))
print("failed_count =", len(failed))
print("report =", out)
