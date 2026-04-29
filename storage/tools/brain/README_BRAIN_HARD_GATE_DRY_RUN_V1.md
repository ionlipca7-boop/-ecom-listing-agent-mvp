# README_BRAIN_HARD_GATE_DRY_RUN_V1

Status: FEATURE_BRANCH_IMPLEMENTATION
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
This package implements the first dry-run Brain Hard-Gate layer for ECOM OS.

It is designed to validate governance decisions before any live integration.

## Package path

```text
storage/tools/brain/
```

## Implemented modules

```text
__init__.py
action_request_loader.py
approval_guard.py
audit_writer.py
brain_hard_gate.py
dry_run_validator.py
environment_guard.py
forbidden_path_guard.py
operator_message_ru.py
pointer_loader.py
schemas.py
verification_guard.py
```

## Safety guarantee
The dry-run package must not:
- call eBay live APIs
- call server runtime
- read secrets
- publish
- revise
- delete
- mutate inventory
- enable ads
- send live offers

## Decision flow

```text
Pointer Loader
  -> Action Request Loader
  -> Environment Guard
  -> Forbidden Path Guard
  -> next_allowed_action check
  -> Approval Guard
  -> Verification Guard
  -> Audit Writer
  -> Russian Operator Message
```

## Main entry point

```python
from storage.tools.brain.brain_hard_gate import evaluate_action
```

## Dry-run validator

```python
from storage.tools.brain.dry_run_validator import run_dry_run
```

The validator checks:
1. safe read-only route
2. Telegram publish-like action without approval blocked
3. GitHub audit -> server runtime blocked
4. approved live-like action returns dry-run only

## Expected safety flags
Every dry-run decision must keep:

```json
{
  "live_called": false,
  "server_touched": false,
  "publish_called": false
}
```

## Audit output
Decision audit:

```text
storage/state_control/brain_hard_gate_decision_v1.json
```

Dry-run result:

```text
storage/state_control/brain_hard_gate_dry_run_result_v1.json
```

## Next step
Run local dry-run verification in a controlled environment before any integration with existing runtime.

STOP: Do not connect this package to live routes until dry-run PASS is reviewed.
