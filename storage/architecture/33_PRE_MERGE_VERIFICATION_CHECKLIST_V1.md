# 33_PRE_MERGE_VERIFICATION_CHECKLIST_V1

Status: PRE_MERGE_REVIEW_CHECKLIST
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the verification checklist before any PR/merge consideration for Brain Hard-Gate dry-run.

## Internet-aligned checks
This checklist follows current engineering/security practices:
- protected branches and required checks before merging;
- pull request review before main changes;
- fail-secure behavior;
- no sensitive data in errors/logs;
- least privilege and explicit boundaries;
- dry-run before integration.

## 1. Branch safety
PASS if:
- branch is feature/brain-hard-gate-dry-run-v1;
- branch is ahead of main only with Brain package files;
- branch is not behind main;
- no existing runtime files were modified.

## 2. File scope
Allowed paths:
```text
storage/tools/brain/
storage/architecture/
```

FAIL if any of these changed:
```text
.env
storage/secrets/
server runtime scripts
existing eBay live scripts
existing Telegram runtime scripts
```

## 3. Import safety
PASS if Brain package imports only standard library and internal Brain modules.
FAIL if Brain imports:
- eBay adapter;
- Telegram runtime;
- server runtime;
- secrets loader;
- inventory mutation module.

## 4. Dry-run execution
Command:
```text
python -m storage.tools.brain.dry_run_validator
```

Expected:
```text
status = PASS
live_called = false
server_touched = false
publish_called = false
```

## 5. Audit output
Verify files:
```text
storage/state_control/brain_hard_gate_decision_v1.json
storage/state_control/brain_hard_gate_dry_run_result_v1.json
```

PASS if:
- valid JSON;
- UTF-8 readable;
- contains safety flags;
- contains Russian operator message;
- contains no secrets/tokens.

## 6. Failure behavior
PASS if:
- missing pointer => CHECK_REQUIRED;
- invalid request => BLOCK;
- unknown environment => BLOCK;
- live action without approval => BLOCK;
- approved live-like action in dry-run => ALLOW_DRY_RUN_ONLY.

## 7. Main protection rule
Do not merge to main until:
- dry-run PASS is reviewed;
- operator approves merge;
- PR is reviewed;
- no live dependency appears;
- no server touch is required.

## 8. STOP conditions
STOP immediately if:
- any live path is imported;
- any secret-like value appears in audit;
- any publish/server flag becomes true;
- dry-run mutates real inventory;
- branch modifies existing live runtime files;
- test requires server or marketplace credentials.

## Current recommendation
Do not merge yet. Next step is local isolated dry-run execution and result review.
