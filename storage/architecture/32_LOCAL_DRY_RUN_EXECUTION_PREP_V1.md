# 32_LOCAL_DRY_RUN_EXECUTION_PREP_V1

Status: LOCAL_EXECUTION_PREP
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Prepare the first controlled local dry-run execution review for Brain Hard-Gate.

## Internet-aligned controls
The preparation follows:
- least privilege;
- secure defaults;
- fail secure;
- explicit boundaries;
- no secrets in logs;
- protected branch / review before merge;
- dry-run before integration.

## Execution location
Recommended first execution:

```text
LOCAL WINDOWS or isolated local clone
```

Not allowed for first dry-run:

```text
SERVER_RUNTIME
TELEGRAM_RUNTIME
LIVE MARKETPLACE PATH
```

## Pre-run checklist

### 1. Branch check
Confirm current branch:

```text
feature/brain-hard-gate-dry-run-v1
```

### 2. File scope check
Confirm changed files are only under:

```text
storage/tools/brain/
storage/architecture/
```

### 3. No secret check
Confirm no `.env`, token, or secret file is touched.

### 4. Import safety check
Confirm Brain package does not import:
- eBay live adapter;
- server runtime scripts;
- Telegram runtime process;
- inventory mutation module;
- secret reader.

### 5. Dry-run command
First local command should execute only:

```text
python -m storage.tools.brain.dry_run_validator
```

### 6. Expected result
Expected status:

```text
PASS
```

Expected safety flags:

```json
{
  "live_called": false,
  "server_touched": false,
  "publish_called": false
}
```

## Expected generated files

```text
storage/state_control/brain_hard_gate_decision_v1.json
storage/state_control/brain_hard_gate_dry_run_result_v1.json
```

## PASS conditions
- All dry-run test cases pass.
- No live calls.
- No server touch.
- No publish call.
- Audit JSON exists.
- Russian operator message exists.
- No existing runtime/source file modified.

## FAIL conditions
Stop if:
- import error occurs;
- dry-run calls live path;
- server path touched;
- publish flag becomes true;
- secret-like value appears in audit;
- current pointer is overwritten in real working project without temporary isolation.

## Important isolation warning
The dry-run validator currently creates a safe pointer inside the provided root. For safest first execution, run in a temporary local copy or test root before running in the real project root.

## Next step after PASS
1. Review dry-run result JSON.
2. Review decision audit JSON.
3. Confirm safety flags false.
4. Create PR from feature branch if review is clean.
5. Do not merge to main until operator approval.

STOP: This document prepares execution only. It does not authorize live integration.
