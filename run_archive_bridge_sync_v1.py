import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "storage" / "memory" / "archive" / "archive_bridge_sync_audit_v1.json"

def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, shell=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

def main():
    result = {}
    rc, out, err = run("py run_build_archive_index_v1.py")
    result["index_build_rc"] = rc
    result["index_build_out"] = out
    result["index_build_err"] = err
    rc, out, err = run("git rev-parse --abbrev-ref HEAD")
    branch = out if rc == 0 and out else "unknown"
    result["branch"] = branch
    result["branch_rc"] = rc
    rc, out, err = run("git add storage\\memory\\archive")
    result["git_add_rc"] = rc
    result["git_add_out"] = out
    result["git_add_err"] = err
    rc, out, err = run("git diff --cached --quiet")
    has_changes = bool(rc)
    result["diff_rc"] = rc
    result["has_changes"] = has_changes
    commit_created = False
    push_rc = int("0")
    push_out = ""
    push_err = ""
    if has_changes:
        rc, out, err = run('git commit -m "archive sync v1"')
        result["git_commit_rc"] = rc
        result["git_commit_out"] = out
        result["git_commit_err"] = err
        commit_created = (rc == 0)
        if commit_created and branch != "unknown":
            push_rc, push_out, push_err = run("git push origin " + branch)
    else:
        result["git_commit_rc"] = int("0")
        result["git_commit_out"] = "no_changes"
        result["git_commit_err"] = ""
    result["commit_created"] = commit_created
    result["git_push_rc"] = push_rc
    result["git_push_out"] = push_out
    result["git_push_err"] = push_err
    ok_index = (result["index_build_rc"] == 0)
    ok_add = (result["git_add_rc"] == 0)
    ok_push = (push_rc == 0)
    result["status"] = "OK" if ok_index and ok_add and ok_push else "CHECK"
    result["decision"] = "archive_bridge_sync_v1_completed"
    AUDIT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("ARCHIVE_BRIDGE_SYNC_V1_AUDIT")
    print("status =", result["status"])
    print("branch =", result["branch"])
    print("has_changes =", result["has_changes"])
    print("commit_created =", result["commit_created"])
    print("git_push_rc =", result["git_push_rc"])

if __name__ == "__main__":
    main()
