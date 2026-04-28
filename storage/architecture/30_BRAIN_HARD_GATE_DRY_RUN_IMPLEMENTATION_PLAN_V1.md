# 30_BRAIN_HARD_GATE_DRY_RUN_IMPLEMENTATION_PLAN_V1

Status: READY_FOR_CONTROLLED_IMPLEMENTATION
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the first safe implementation plan for Brain Hard-Gate dry-run, before any connection to live runtime.

## Core rule
First implementation must be local/dry-run only. It must not call eBay, Telegram runtime, server runtime, inventory mutation, ads, offers, revise, delete, or publish.

---

# 1. Implementation target

Create a minimal Brain Hard-Gate dry-run package under:

```text
storage/tools/brain/
```

Initial files:

```text
schemas.py
pointer_loader.py
action_request_loader.py
approval_guard.py
environment_guard.py
forbidden_path_guard.py
verification_guard.py
audit_writer.py
operator_message_ru.py
brain_hard_gate.py
dry_run_validator.py
```

No existing production scripts should be modified in the first dry-run implementation.

---

# 2. First branch strategy

Recommended implementation branch:

```text
feature/brain-hard-gate-dry-run-v1
```

Rules:
- Do not implement directly on main.
- Do not implement directly on server runtime.
- Do not merge until dry-run PASS is verified.
- Keep architecture-audit-v1 as planning branch.

---

# 3. Execution order

## Step 1 — Create module folder
Create:

```text
storage/tools/brain/
```

Add minimal `__init__.py`.

Verification:
- folder exists
- no runtime/live imports

## Step 2 — Add schemas.py
Add constants for:
- valid environments
- valid risk levels
- decision statuses
- approval-required risk levels

Verification:
- import schemas works
- no external calls

## Step 3 — Add pointer_loader.py
Read:

```text
storage/control_room/CURRENT_POINTER.json
```

Behavior:
- missing file -> CHECK_REQUIRED
- invalid JSON -> BLOCK
- missing next_allowed_action -> CHECK_REQUIRED

Verification:
- handles missing file safely
- handles valid JSON safely

## Step 4 — Add action_request_loader.py
Read optional action request file or accept inline request object.

Verification:
- invalid request -> BLOCK
- unknown environment -> BLOCK
- unknown risk -> BLOCK

## Step 5 — Add environment_guard.py
Implement environment/action compatibility rules.

Verification:
- GITHUB_AUDIT cannot server runtime
- TELEGRAM_INTERFACE cannot direct eBay live
- LOCAL_WINDOWS cannot assume server secrets

## Step 6 — Add approval_guard.py
Implement approval requirement logic.

Verification:
- live without approval -> BLOCK
- dangerous without approval -> BLOCK
- read_only no approval -> allowed to continue checks

## Step 7 — Add forbidden_path_guard.py
Encode forbidden direct paths.

Verification:
- Telegram -> eBay live blocked
- Inventory -> marketplace mutation blocked
- agent bypass Brain blocked

## Step 8 — Add verification_guard.py
Return verification requirement for live/risky actions.

Verification:
- publish requires visibility verify
- quantity sync requires consistency verify
- token refresh requires token verify

## Step 9 — Add audit_writer.py
Write decision JSON to:

```text
storage/state_control/brain_hard_gate_decision_v1.json
```

Safety fields must exist and default to false:
- live_called
- server_touched
- publish_called

## Step 10 — Add operator_message_ru.py
Return short Russian operator message for each decision.

Verification:
- BLOCK messages are clear
- no secret values
- no long technical noise

## Step 11 — Add brain_hard_gate.py
Orchestrate:

```text
load pointer
load request
check environment
check forbidden paths
check next_allowed_action
check approval
check verification
write audit
return decision
```

## Step 12 — Add dry_run_validator.py
Run four test cases:
1. safe read-only
2. publish without approval
3. wrong environment
4. approved live simulation as ALLOW_DRY_RUN_ONLY

Verification:
- no live calls
- no server touch
- no publish
- audit written
- PASS/FAIL result written

---

# 4. Dry-run output

Write:

```text
storage/state_control/brain_hard_gate_dry_run_result_v1.json
```

Required summary:

```json
{
  "status": "PASS | FAIL | CHECK_REQUIRED",
  "summary": {
    "live_called": false,
    "server_touched": false,
    "publish_called": false
  }
}
```

---

# 5. Stop gates

Stop immediately if:
- any implementation tries to import eBay live code;
- any implementation touches server runtime;
- any implementation tries to read secrets;
- any dry-run calls publish/revise/delete;
- any dry-run mutates inventory;
- pointer cannot be read and behavior is not CHECK_REQUIRED/BLOCK;
- audit cannot be written safely.

---

# 6. Rollback rule

Because first implementation is additive only, rollback is simple:
- remove storage/tools/brain/ from feature branch;
- remove generated dry-run state files if created during testing;
- do not touch main.

No live rollback should be needed because no live action is allowed.

---

# 7. Success condition

Brain Hard-Gate dry-run implementation is ready when:
- all 4 test cases pass;
- generated audit contains safety flags;
- live_called=false;
- server_touched=false;
- publish_called=false;
- Russian operator messages exist;
- no existing production file was modified.

---

# 8. Next phase after PASS

After dry-run PASS:
1. Review result.
2. Create integration plan.
3. Connect Brain only to read-only route first.
4. Do not connect live publish until approval and visibility verify gate are confirmed.

STOP: This file is the dry-run implementation plan only. It does not execute code.
