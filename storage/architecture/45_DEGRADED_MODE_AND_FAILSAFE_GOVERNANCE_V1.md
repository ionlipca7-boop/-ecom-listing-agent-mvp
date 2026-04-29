# 45_DEGRADED_MODE_AND_FAILSAFE_GOVERNANCE_V1

Status: DEGRADED_MODE_FAILSAFE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define degraded mode and failsafe governance for ECOM OS.

## Core principle
If uncertainty increases, capability must decrease.

## Degraded modes
Possible modes:
- READ_ONLY_MODE;
- DRAFT_ONLY_MODE;
- APPROVAL_ONLY_MODE;
- MARKETPLACE_PAUSED_MODE;
- INVENTORY_RECONCILIATION_MODE;
- RECOVERY_ONLY_MODE.

## Trigger examples
Enter degraded mode if:
- inventory mismatch detected;
- token health unstable;
- marketplace adapter unstable;
- audit missing;
- verification missing;
- repeated recovery failures;
- stale state detected.

## Failsafe rules
In degraded mode:
- no automatic publish;
- no automatic revise;
- no automatic delete;
- no automatic price mutation;
- no inventory mutation without verification.

## Operator visibility
Operator must receive:
- degraded reason;
- affected subsystem;
- blocked capabilities;
- recommended next step.

## Recovery exit
Exit degraded mode only after:
- verification passes;
- audit written;
- operator aware;
- health restored.

STOP: This document defines degraded/failsafe governance only.
