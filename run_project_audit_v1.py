import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "storage" / "exports"
OUTPUT_FILE = EXPORTS_DIR / "project_audit_v1.json"
def rel_list(paths):
    return [str(p.relative_to(BASE_DIR)) for p in sorted(paths)]
def main():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    py_files = rel_list(BASE_DIR.glob("*.py"))
    secret_files = rel_list((BASE_DIR / "storage" / "secrets").glob("*")) if (BASE_DIR / "storage" / "secrets").exists() else []
    export_files = rel_list((BASE_DIR / "storage" / "exports").glob("*")) if (BASE_DIR / "storage" / "exports").exists() else []
    run_files = [x for x in py_files if x.startswith("run_")]
    token_like = [x for x in secret_files if "token" in x.lower() or "secret" in x.lower() or "client" in x.lower() or "redirect" in x.lower()]
    result = {"status": "OK", "project_root": str(BASE_DIR), "py_files_count": len(py_files), "run_files_count": len(run_files), "secret_files_count": len(secret_files), "export_files_count": len(export_files), "py_files": py_files, "run_files": run_files, "secret_files": secret_files, "token_like_secret_files": token_like, "export_files": export_files}
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("PROJECT_AUDIT_V1_DONE")
    print("py_files_count =", len(py_files))
    print("run_files_count =", len(run_files))
    print("secret_files_count =", len(secret_files))
    print("export_files_count =", len(export_files))
if __name__ == "__main__":
    main()
