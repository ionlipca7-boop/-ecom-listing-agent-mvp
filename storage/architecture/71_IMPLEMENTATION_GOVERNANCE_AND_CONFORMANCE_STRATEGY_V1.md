# 71_IMPLEMENTATION_GOVERNANCE_AND_CONFORMANCE_STRATEGY_V1

Status: IMPLEMENTATION_GOVERNANCE_CONFORMANCE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define implementation governance so production code preserves architecture intent.

## External practice alignment
This strategy follows:
- architecture conformance checking;
- continuous architecture validation;
- implementation review discipline;
- guardrail-based engineering;
- safe deployment practices.

## Core decision
Implementation must conform to architecture, not bypass it.

## Implementation rules
All implementation work must:
- preserve Brain governance boundaries;
- preserve adapter isolation;
- preserve inventory single source of truth;
- preserve approval and verification gates;
- write audit for important decisions;
- remain environment-aware;
- avoid secret leakage.

## Review checks
Before merge/integration verify:
- no direct live route was introduced;
- no secret reader was added to dry-run code;
- Brain did not import marketplace clients;
- adapters did not own global governance;
- inventory truth did not split;
- audit path exists.

## Conformance evidence
Required evidence:
- tests or dry-run result;
- diff review;
- architecture checklist pass;
- risk notes;
- rollback plan if runtime-affecting.

## STOP conditions
STOP if:
- implementation bypasses Brain;
- architecture boundary is violated;
- undocumented runtime shortcut appears;
- feature moves to live without readiness evidence.

STOP: This document defines implementation governance only.
