# 26_BRAIN_HARD_GATE_IMPLEMENTATION_TASKS_V1

Status: IMPLEMENTATION_TASKS_DRAFT
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Convert Brain Hard-Gate specification into concrete implementation tasks.

## Scope
This task list is for planning and controlled implementation only. It does not modify runtime behavior yet.

---

# TASK GROUP A — Discover Current Control Files

## A1. Locate current pointer/state files
Goal:
- Identify exact current control files used by the existing project.

Expected files/patterns:
- storage/control_room/CURRENT_POINTER.json
- storage/state_control/*.json
- storage/rules/*.json

Verification:
- File exists.
- JSON is readable.
- Contains current_position or next_allowed_action when applicable.

Stop condition:
- If pointer is missing, do not continue to runtime implementation.

Risk: Medium

---

# TASK GROUP B — Define Brain Gate Input Contract

## B1. Define action request schema
Brain must receive a structured action request.

Draft schema:
```json
{
  "requested_action": "",
  "requested_by": "operator | telegram | system | tool",
  "environment": "LOCAL_WINDOWS | GITHUB_AUDIT | SERVER_RUNTIME | TELEGRAM_INTERFACE",
  "target_module": "",
  "risk_level": "read_only | draft | live | dangerous",
  "approval_reference": null,
  "requires_verification": true
}
```

Verification:
- Schema supports read-only, draft, live, dangerous actions.
- Schema includes environment.
- Schema includes approval reference.

Risk: Medium

---

# TASK GROUP C — Pointer Enforcement

## C1. Implement next_allowed_action check
Brain must compare requested_action with current next_allowed_action.

Pass:
- requested_action == next_allowed_action

Fail:
- missing next_allowed_action
- mismatched requested_action
- invalid pointer JSON

Output:
- ALLOW or BLOCK
- reason
- audit event

Risk: High

---

# TASK GROUP D — Approval Enforcement

## D1. Define approval-required actions
Approval required:
- publish
- revise
- delete
- send live offer
- enable live ads
- dangerous inventory mutation
- server live runtime change

## D2. Implement approval check
Brain must check approval_reference before live/dangerous action.

Fail behavior:
- BLOCK
- write audit
- Russian operator message

Risk: High

---

# TASK GROUP E — Environment Enforcement

## E1. Define allowed environment/action matrix
Examples:
- GITHUB_AUDIT: docs, branches, PRs only
- LOCAL_WINDOWS: engineering, local audit, safe scripts
- SERVER_RUNTIME: runtime execution, secrets, live adapters
- TELEGRAM_INTERFACE: commands, approvals, notifications

## E2. Block invalid environment paths
Examples:
- GITHUB_AUDIT cannot publish
- TELEGRAM_INTERFACE cannot directly call eBay adapter
- LOCAL_WINDOWS cannot assume server secrets

Risk: High

---

# TASK GROUP F — Forbidden Path Rules

## F1. Encode forbidden direct paths
Forbidden:
- Telegram -> eBay direct publish
- Inventory -> marketplace direct mutation
- Marketplace adapter -> inventory truth ownership
- Agent -> bypass Brain
- Any module -> secrets print

Output:
- forbidden_path_detected true/false
- reason
- stop_required true/false

Risk: High

---

# TASK GROUP G — Verification Requirement

## G1. Define verification-required actions
Verification required after:
- publish
- revise
- quantity sync
- offer send
- ad enable/disable
- token refresh
- server runtime restart

## G2. Require verify result before next phase
Brain must not advance route without required verification.

Risk: High

---

# TASK GROUP H — Audit Events

## H1. Define Brain audit schema
```json
{
  "status": "ALLOW | BLOCK | CHECK_REQUIRED",
  "layer": "BRAIN_HARD_GATE_V1",
  "requested_action": "",
  "next_allowed_action": "",
  "environment": "",
  "risk_level": "",
  "approval_required": false,
  "approval_present": false,
  "verification_required": false,
  "decision_reason": "",
  "timestamp": ""
}
```

## H2. Write audit file
Target:
- storage/state_control/brain_hard_gate_decision_v1.json

Risk: Medium

---

# TASK GROUP I — Russian Operator Message

## I1. Define response text rules
Brain must return short Russian messages:
- allowed
- blocked
- missing approval
- wrong environment
- missing verification
- missing pointer

Example:
"Блокировано: действие publish требует approval gate. Live publish не запускался."

Risk: Low

---

# TASK GROUP J — Dry-Run Validator

## J1. Build dry-run mode first
Before connecting Brain to runtime, create dry-run check.

Dry-run must:
- read pointer
- evaluate one fake action
- write audit
- call no live adapter

Success condition:
- dry-run blocks invalid publish without approval
- dry-run allows matching read-only action

Risk: Medium

---

# Implementation order
1. A — discover current control files
2. B — define request schema
3. C — pointer enforcement
4. D — approval enforcement
5. E — environment enforcement
6. F — forbidden path rules
7. G — verification requirements
8. H — audit events
9. I — Russian messages
10. J — dry-run validator

---

# Global stop conditions
Stop if:
- pointer missing
- approval model unclear
- runtime environment unclear
- action is live but verification path missing
- any step tries to publish/revise/delete during planning

---

# Finish condition
Brain Hard-Gate task planning is complete when:
- request schema exists
- enforcement tasks are ordered
- audit schema exists
- dry-run validator is defined
- no live action is required for first implementation

STOP: This file is planning only. No runtime change from this file.
