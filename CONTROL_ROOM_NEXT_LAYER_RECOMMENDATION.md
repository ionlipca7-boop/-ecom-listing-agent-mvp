# ECOM LISTING AGENT MVP — Safest Next Layer Before Merge

## 1) Short analysis
Current local repository state **does not match** the provided "confirmed state" snapshot:
- Working tree is clean (`git status --short` returned nothing).
- Current branch is `work` (not `generator-layer-v2`).
- Latest local commit is `21aedc1` (not `bbacfba`).

Given this mismatch, the safest move is to run a **publish-artifact governance layer** (read-only classification + guardrails) before any merge.

## 2) Codex chat: SAME or NEW
**SAME**.
Continue in the same chat so provenance of the mismatch and verification commands stays in one audit trail.

## 3) GitHub: MERGE or NO MERGE
**NO MERGE** (for now).
Do not merge until the branch/package state is re-verified against the expected snapshot and artifact policy is explicitly enforced.

## 4) Exact next CMD commands
```bat
:: 0) Verify branch and cleanliness
cd /d <repo_root>
git branch --show-current
git status --short

:: 1) Refresh from remote and inspect expected branch/commit
git fetch --all --prune
git branch -a
git log --oneline --decorate --all | findstr /i "bbacfba generator-layer-v2"

:: 2) If branch exists remotely, inspect it WITHOUT mutating files
git switch --detach origin/generator-layer-v2

git status --short
git log -1 --oneline

:: 3) Classify artifacts for package_20260414_070314
python - <<PY
import os, json
base = r"publish_packages\\package_20260414_070314"
if os.path.isdir(base):
    files = sorted(os.listdir(base))
    print("package files:", len(files))
    for f in files:
        print(f)
else:
    print("MISSING:", base)
PY

:: 4) Run quick safety checks (read-only)
python generate_ebay_template_output_v2.py
python validate_ebay_template_output_v2.py

:: 5) Return to working branch
git switch -
```

## 5) Safest cleanup/review recommendation
Use a **two-phase policy** before merge:

1. **Keep (required artifacts, likely commit-worthy in release packaging):**
   - Core mapping/template outputs and validation summaries tied to the confirmed package.
   - Final human/audit JSON summaries that prove upload readiness.

2. **Exclude now (temporary noise, should be gitignored or staged later):**
   - Derived feeds (`ebay_feed*.csv`) and intermediate bundle expansion folders.
   - Zips and regenerated exports unless the repo explicitly versions release bundles.
   - Transient logs/manifests that are reproducible from scripts.

3. **Decision gate (before merge):**
   - Add/confirm `.gitignore` rules for reproducible temporary outputs.
   - Keep a minimal auditable set: source scripts + deterministic final validation summaries.
   - If unsure, prefer "do not delete, do not commit" and park uncertain files in a review checklist PR comment.

4. **Merge readiness criterion:**
   - Reproduce `validation_ok=true`, `columns_count=96`, `rows_count=7`, missing-title/price = 0 on the target branch.
   - Confirm quick-run still passes after cleanup policy is applied.
