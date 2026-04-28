# 25_BRAIN_HARD_GATE_IMPLEMENTATION_SPEC_V1

Status: IMPLEMENTATION_START_SPEC
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Brain Hard-Gate is the first implementation target. It is not a new AI layer. It is a governed control router that blocks unsafe actions and allows only valid next steps.

## Core responsibilities

### 1. Current Pointer Enforcement
Brain must read the current pointer/state and enforce next_allowed_action. If the requested action does not match the allowed route, Brain must stop and write an audit event.

### 2. Approval Enforcement
Brain must block publish, revise, delete, live ads, live offers, and risky inventory mutation unless the correct approval gate is open.

### 3. Environment Awareness
Brain must know whether the requested action belongs to LOCAL_WINDOWS, GITHUB_AUDIT, SERVER_RUNTIME, or TELEGRAM_INTERFACE.

Rules:
- GitHub audit cannot execute runtime.
- Telegram cannot publish directly.
- Server runtime cannot rewrite architecture.
- Local Windows is engineering/operator workspace.

### 4. Forbidden Path Blocking
Forbidden paths:
- Telegram -> eBay direct publish
- Inventory -> marketplace direct mutation
- Agent -> bypass Brain
- Marketplace adapter -> own inventory truth
- Runtime script -> bypass verification

### 5. Verify-First Enforcement
Brain must require verification before continuation. API success is not business success. Publish success is not active listing visibility. Quantity sync success is not marketplace reality until verified.

### 6. Audit Hooks
Brain must write decision, route, environment, approval, verification, and recovery audit events.

## Runtime flow

```text
Telegram / Operator
  -> Telegram RU Operator Layer
  -> Brain Hard-Gate
  -> Pointer Validation
  -> Approval Check
  -> Environment Check
  -> Target Module Dispatch
  -> Verification
  -> Audit Write
  -> Telegram Response
```

## Minimal first implementation scope
Allowed:
- route checks
- approval checks
- environment checks
- forbidden path checks
- audit generation
- verification-required flags

Forbidden:
- giant rewrite
- new autonomous AI execution
- distributed orchestration
- multi-agent runtime
- live action changes
- server changes during spec phase

## Failure handling
If violation is detected:
1. STOP
2. Do not continue automatically
3. Write audit event
4. Notify operator in Russian

Examples:
- missing pointer
- invalid next_allowed_action
- missing approval
- wrong environment
- missing verification

## Dependencies
Brain depends on:
- current state/pointer
- approval gate
- audit/memory
- recovery playbooks

Brain must not depend on:
- marketplace-specific payload details
- Telegram UI rendering
- future AI agents
- predictive systems

## Success conditions
This phase is successful when:
- invalid route is blocked
- missing approval is blocked
- wrong environment is blocked
- verification is required before continuation
- audit file is created for every decision
- operator receives Russian explanation

## Next phase after success
Inventory Sales Core stabilization.

STOP: This is a specification file only. No runtime change from this file.
