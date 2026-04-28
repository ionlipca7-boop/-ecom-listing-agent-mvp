# 48_N8N_AND_EXTERNAL_AUTOMATION_BRIDGE_ARCHITECTURE_V1

Status: N8N_EXTERNAL_BRIDGE_ARCHITECTURE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define governance and security boundaries for n8n and external automation bridges.

## External practice alignment
This strategy follows:
- webhook isolation;
- credential separation;
- least privilege;
- hardened workflow boundaries;
- environment separation;
- workflow auditability.

## Core decision
n8n/external automation is a bridge layer, not a governance owner.

## Security boundaries
n8n must not:
- own Brain governance;
- store unrestricted production secrets;
- directly bypass approval gates;
- execute unrestricted marketplace actions.

## Environment separation
Required separation:
- TEST workflows;
- DRY RUN workflows;
- PRODUCTION workflows.

Credentials must be separated.

## Webhook governance
All external webhooks must pass:
- signature/auth validation;
- source validation;
- Brain governance check;
- audit logging.

## Allowed external actions
Allowed:
- notifications;
- queue triggers;
- draft preparation;
- safe read-only checks;
- workflow orchestration.

Requires approval:
- marketplace live actions;
- inventory mutation;
- finance export finalization;
- price mutation.

## STOP conditions
STOP if:
- workflow has unrestricted production credential access;
- webhook bypasses Brain;
- workflow directly publishes without approval;
- workflow runtime is unpatched/untrusted.

STOP: This document defines external automation governance only.
