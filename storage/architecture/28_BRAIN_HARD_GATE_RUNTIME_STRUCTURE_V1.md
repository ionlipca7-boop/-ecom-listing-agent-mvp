# 28_BRAIN_HARD_GATE_RUNTIME_STRUCTURE_V1

Status: RUNTIME_STRUCTURE_DRAFT
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define where Brain Hard-Gate lives in the project, which files it may read/write, and which runtime boundaries it must respect.

## Practice check
This structure follows the incremental modernization idea: introduce a control router/gate around existing behavior before replacing or expanding runtime logic. This avoids a big rewrite and keeps existing project behavior protected.

## Runtime locations

### Control room
Path:
```text
storage/control_room/
```
Owns:
- CURRENT_POINTER.json
- current route state
- next_allowed_action
- current_position

Brain may read this path.
Brain may not silently overwrite pointer without explicit route update step.

### State control
Path:
```text
storage/state_control/
```
Owns:
- Brain decisions
- dry-run audit
- validation results
- verification results
- recovery check results

Brain may write audit JSON here.

### Rules
Path:
```text
storage/rules/
```
Owns:
- controlled automation rules
- environment rules
- approval rules
- forbidden path rules

Brain may read rules here.
Brain may not mutate rules during normal action check.

### Archive memory
Path:
```text
storage/memory/archive/
```
Owns:
- transitions
- long-term history
- recovery history
- ADR / audit history

Brain may write final archive snapshots only after confirmed checkpoint.

### Brain module root
Future implementation path:
```text
storage/tools/brain/
```
Suggested files:
- pointer_loader.py
- action_request_schema.py
- approval_guard.py
- environment_guard.py
- forbidden_path_guard.py
- verification_guard.py
- audit_writer.py
- dry_run_validator.py

### Recovery module root
Future implementation path:
```text
storage/tools/recovery/
```
Suggested files:
- token_recovery.py
- visibility_recovery.py
- inventory_sync_recovery.py
- runtime_path_recovery.py

## Brain boundaries

Brain CAN:
- read pointer/current state
- read rules
- evaluate requested action
- block unsafe path
- write audit decision
- require verification
- return Russian operator message

Brain CANNOT:
- publish directly
- revise/delete directly
- mutate inventory directly
- own marketplace payload logic
- print secrets
- bypass approval
- bypass verification

## Environment ownership

### GITHUB_AUDIT
Allowed:
- architecture docs
- branches
- PRs
- read-only source audit

Forbidden:
- server runtime actions
- marketplace API calls
- secret access

### LOCAL_WINDOWS
Allowed:
- engineering checks
- local dry-runs
- source inspection

Forbidden:
- assuming server secrets exist locally
- live actions without explicit server gate

### SERVER_RUNTIME
Allowed:
- runtime execution
- secrets access from .env
- Telegram bot runtime
- marketplace adapters

Forbidden:
- architecture rewrite
- printing secrets
- live actions without Brain + approval

### TELEGRAM_INTERFACE
Allowed:
- operator messages
- approvals
- notifications

Forbidden:
- direct marketplace actions
- direct inventory mutation

## Minimal runtime decision file
Target:
```text
storage/state_control/brain_hard_gate_decision_v1.json
```

Must include:
- status
- requested_action
- next_allowed_action
- environment
- target_module
- approval_required
- approval_present
- forbidden_path_detected
- verification_required
- decision_reason
- live_called false/true
- timestamp

## First implementation principle
Build Brain Hard-Gate as a wrapper/router around existing behavior first. Do not rewrite the existing system. Do not move modules yet. Do not connect future agents yet.

## Success condition
Runtime structure is accepted when every Brain read/write path is explicit and every forbidden environment/action path is documented.

STOP: This file defines runtime structure only. It does not execute runtime code.
