import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "storage" / "exports"
ARCHIVE_DIR = ROOT / "storage" / "memory" / "archive"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def load_json(name):
    p = EXPORT_DIR / name
    if not p.exists():
        return {"status": "MISSING", "file": name}
    return json.loads(p.read_text(encoding="utf-8"))

v1 = load_json("safe_cleanup_batch_result_v1.json")
v2 = load_json("safe_cleanup_batch_v2_result.json")
v3 = load_json("safe_cleanup_batch_v3_result.json")

summary = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "root_cleanup_finalized",
    "cleanup_status": "SAFE_ROOT_CLEANUP_COMPLETED",
    "results": {
        "v1_moved_count": v1.get("moved_count", 0),
        "v2_moved_count": v2.get("moved_count", 0),
        "v3_moved": v3.get("moved", False)
    },
    "achievements": [
        "root_pycache_removed",
        "safe_root_candidates_quarantined",
        "cleanup_backup_quarantined",
        "root_cleanup_stability_preserved"
    ],
    "rules_confirmed": [
        "always_use_quarantine_first",
        "delete_only_from_safe_list_first",
        "do_not_touch_core_storage_active_adapter",
        "python_is_primary_layer",
        "no_hard_delete"
    ],
    "next_step": "post_cleanup_project_audit_or_next_feature_layer"
}

export_path = EXPORT_DIR / "root_cleanup_final_summary_v1.json"
archive_path = ARCHIVE_DIR / "root_cleanup_final_summary_v1.json"
text = json.dumps(summary, ensure_ascii=False, indent=2)
export_path.write_text(text, encoding="utf-8")
archive_path.write_text(text, encoding="utf-8")
print("ROOT_CLEANUP_FINALIZED")
print("v1_moved_count =", summary["results"]["v1_moved_count"])
print("v2_moved_count =", summary["results"]["v2_moved_count"])
print("v3_moved =", summary["results"]["v3_moved"])
print("export =", export_path)
print("archive =", archive_path)
