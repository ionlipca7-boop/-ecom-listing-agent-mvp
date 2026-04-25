import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "storage" / "exports" / "listing_clone_execution_plan_v1.json"
EXPORT_DIR = BASE_DIR / "storage" / "exports"
ARCHIVE_DIR = BASE_DIR / "storage" / "memory" / "archive"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = EXPORT_DIR / "archive_and_github_sync_v1.json"
ARCHIVE_COPY_PATH = ARCHIVE_DIR / "archive_and_github_sync_v1.json"

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)
    result = {
        "status": "OK",
        "decision": "archive_and_github_sync_v1_built",
        "project": "ECOM_LISTING_AGENT_MVP_CONTROL_ROOM",
        "archive_and_github_sync_version": "v1",
        "template_key": source.get("template_key"),
        "baseline_sku": source.get("baseline_sku"),
        "baseline_offer_id": source.get("baseline_offer_id"),
        "baseline_image_count": source.get("baseline_image_count", 0),
        "archive_contract": {
            "save_local_archive": True,
            "verify_archive_after_write": True,
            "archive_after_success": True,
            "preserve_phase_history": True
        },
        "github_sync_contract": {
            "github_sync_ready": True,
            "auto_push_now": False,
            "manual_review_before_push": True,
            "use_github_as_backup_not_runtime": True
        },
        "future_flow": [
            "step_success",
            "write_local_archive",
            "verify_archive",
            "prepare_git_status",
            "manual_review",
            "optional_github_push" 
        ],
        "next_step": "archive_multi_listing_system_v1" 
    }
    raw = json.dumps(result, ensure_ascii=False, indent=2)
    OUT_PATH.write_text(raw, encoding="utf-8")
    ARCHIVE_COPY_PATH.write_text(raw, encoding="utf-8")
    print("ARCHIVE_AND_GITHUB_SYNC_V1_FINAL_AUDIT")
    print("status = OK")
    print("decision = archive_and_github_sync_v1_built")
    print("template_key =", result["template_key"])
    print("baseline_image_count =", result["baseline_image_count"])
    print("save_local_archive =", result["archive_contract"]["save_local_archive"])
    print("github_sync_ready =", result["github_sync_contract"]["github_sync_ready"])
    print("auto_push_now =", result["github_sync_contract"]["auto_push_now"])
    print("next_step =", result["next_step"])

if __name__ == "__main__":
    main()
