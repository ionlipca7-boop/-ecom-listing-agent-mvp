# 35_PR_REVIEW_STRUCTURE_V1

Status: PR_REVIEW_STRUCTURE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define how the Brain Hard-Gate dry-run feature branch should be reviewed before any merge to main.

## External practice alignment
This structure follows:
- protected branches;
- required status checks;
- approving review before merge;
- fail secure behavior;
- least privilege;
- explicit trust boundaries;
- dry-run before integration.

## PR title

```text
Add Brain Hard-Gate dry-run governance layer V1
```

## PR type

```text
Draft PR first
```

Reason:
- dry-run needs local result review;
- no merge before operator approval;
- no live integration yet.

## PR summary

The PR should state:
- adds isolated Brain Hard-Gate package under storage/tools/brain/;
- adds dry-run validator;
- does not modify existing runtime files;
- does not call eBay/server/Telegram runtime;
- does not read secrets;
- does not publish/revise/delete;
- requires dry-run PASS before merge consideration.

## Changed paths allowed

Allowed:

```text
storage/tools/brain/
storage/architecture/
```

Not allowed:

```text
.env
storage/secrets/
existing eBay live scripts
existing Telegram runtime scripts
server runtime scripts
inventory data files
```

## Required manual review checklist

### 1. Scope review
- Are all changes additive?
- Are existing files untouched?
- Is this still dry-run only?

### 2. Security review
- No secret reads.
- No token logging.
- No server touch.
- No live API call.
- No unsafe default allow.

### 3. Governance review
- Fail closed behavior exists.
- Approval required for live/dangerous actions.
- Forbidden direct paths are blocked.
- Audit is written.
- Russian operator messages are safe.

### 4. Dry-run review
Required evidence:

```text
storage/state_control/brain_hard_gate_dry_run_result_v1.json
storage/state_control/brain_hard_gate_decision_v1.json
```

Expected:

```text
status=PASS
live_called=false
server_touched=false
publish_called=false
```

### 5. Integration boundary review
Confirm:
- not connected to existing live routes;
- not connected to Telegram runtime yet;
- not connected to eBay adapter yet;
- not connected to inventory mutation yet.

## Merge conditions
Do not merge unless:
1. dry-run PASS is reviewed;
2. operator approves merge;
3. no live dependency appears;
4. PR diff is additive only;
5. no secrets or runtime state appear;
6. next integration plan is read-only first.

## After merge rule
If merged later, next phase must be read-only integration only.

Allowed next integration:

```text
Brain checks read-only route before action
```

Forbidden next integration:

```text
Brain directly executes publish/revise/delete/live adapter
```

## STOP conditions
Stop PR review if:
- live dependency appears;
- safety flags become true;
- existing runtime files were modified unexpectedly;
- dry-run result missing;
- secrets appear;
- server required for tests.

STOP: This file defines PR review structure only. It does not authorize merge.
