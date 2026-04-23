import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
INPUT_FILE = EXPORTS_DIR / "project_audit_v1.json"
OUTPUT_FILE = EXPORTS_DIR / "cleanup_audit_v2.json"

def pick(items, words):
    out = []
    for x in items:
        lx = x.lower()
        if any(w in lx for w in words):
            out.append(x)
    return out

def main():
    data = json.loads(INPUT_FILE.read_text(encoding="utf-8"))
    py_files = data.get("py_files", [])
    export_files = data.get("export_files", [])
    secret_files = data.get("secret_files", [])
    keep_core = pick(py_files, ["control_room.py", "run_control_action_v1.py", "run_increase_live_quantity_v1.py", "run_next_live_pipeline_v1.py", "run_ebay_create_inventory_item_v6.py", "run_ebay_publish_offer_v6.py", "run_ebay_update_offer_v2.py"])
    keep_auth = pick(py_files, ["oauth", "refresh_access_token", "token_smoke_test", "access_token_smoke_test"])
    review_duplicates = [x for x in py_files if "_v1.py" in x or "_v2.py" in x or "_v3.py" in x or "_v4.py" in x or "_v5.py" in x or "_v6.py" in x]
    review_exports_old = export_files
    possible_archive = [x for x in export_files if x.lower().endswith(".json") or x.lower().endswith(".txt")]
    result = {
        "status": "OK",
        "keep_core_count": len(keep_core),
        "keep_auth_count": len(keep_auth),
        "review_duplicates_count": len(review_duplicates),
        "review_exports_old_count": len(review_exports_old),
        "possible_archive_count": len(possible_archive),
        "keep_core": keep_core,
        "keep_auth": keep_auth,
        "secret_files_keep_all_for_now": secret_files,
        "review_duplicates_sample": review_duplicates[:60],
        "possible_archive_sample": possible_archive[:80]
    }
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("CLEANUP_AUDIT_V2_DONE")
    print("keep_core_count =", len(keep_core))
    print("keep_auth_count =", len(keep_auth))
    print("review_duplicates_count =", len(review_duplicates))
    print("review_exports_old_count =", len(review_exports_old))
    print("possible_archive_count =", len(possible_archive))

if __name__ == "__main__":
    main()
