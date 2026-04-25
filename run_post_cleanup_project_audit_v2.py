import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPORT_DIR = ROOT / "storage" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_DIRS = [
    "storage",
    "storage\\exports",
    "storage\\memory",
    "storage\\memory\\archive",
    "storage\\cleanup",
    "agent",
    "app",
    "configs",
    "publisher"
]

REQUIRED_FILES = [
    "run_safe_cleanup_batch_v1.py",
    "run_safe_cleanup_batch_v2.py",
    "run_safe_cleanup_batch_v3.py",
    "run_finalize_root_cleanup_v1.py",
    "storage\\exports\\safe_cleanup_batch_result_v1.json",
    "storage\\exports\\safe_cleanup_batch_v2_result.json",
    "storage\\exports\\safe_cleanup_batch_v3_result.json",
    "storage\\exports\\root_cleanup_final_summary_v1.json",
    "storage\\memory\\archive\\root_cleanup_final_summary_v1.json"
]

dirs_ok = []
dirs_missing = []
files_ok = []
files_missing = []

for rel in REQUIRED_DIRS:
    p = ROOT / rel
    if p.exists() and p.is_dir():
        dirs_ok.append(rel)
    else:
        dirs_missing.append(rel)

for rel in REQUIRED_FILES:
    p = ROOT / rel
    if p.exists() and p.is_file():
        files_ok.append(rel)
    else:
        files_missing.append(rel)

overall_status = "OK" if not dirs_missing and not files_missing else "ATTENTION"

report = {
    "status": "OK",
    "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
    "decision": "post_cleanup_project_audit_v2_completed",
    "overall_status": overall_status,
    "dirs_ok_count": len(dirs_ok),
    "dirs_missing_count": len(dirs_missing),
    "files_ok_count": len(files_ok),
    "files_missing_count": len(files_missing),
    "dirs_missing": dirs_missing,
    "files_missing": files_missing,
    "decision_note": "core_removed_from_required_dirs_for_mvp_structure",
    "next_step": "start_next_feature_layer"
}

out = EXPORT_DIR / "post_cleanup_project_audit_v2.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print("POST_CLEANUP_PROJECT_AUDIT_V2_DONE")
print("overall_status =", overall_status)
print("dirs_missing_count =", len(dirs_missing))
print("files_missing_count =", len(files_missing))
print("report =", out)
