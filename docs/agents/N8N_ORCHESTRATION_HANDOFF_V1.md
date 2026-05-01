# N8N_ORCHESTRATION_HANDOFF_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Define the role of n8n in ECOM OS V3 without allowing uncontrolled automation drift.

n8n is an orchestration layer, not the source of truth and not a blind live executor.

## Position In Canon
Existing control canon order:

1. manifest
2. rules
3. state
4. history
5. control_agent
6. archivist_agent
7. runner_agent
8. n8n_orchestration
9. compact_core_migration

n8n must operate after control/rules/state and before runner actions, under gates.

## Allowed n8n Roles
- receive Telegram command event
- dispatch URL intake step
- dispatch product passport step
- dispatch photo sandbox step
- dispatch title/spec/HTML generation step
- dispatch critic step
- send Telegram preview packet
- record state handoff
- notify operator

## Forbidden n8n Roles
- no live publish without live gate
- no delete/cleanup without cleanup gate
- no server experiments
- no V6/V7/V8 uncontrolled route creation
- no direct eBay revise from unreviewed generated output
- no bypass of Critic Agent

## Required State Handoff
Every n8n step must write or pass:
- route_id
- product_id or SKU
- source packet id
- current layer
- previous status
- next_allowed_action
- artifacts created
- operator approval status
- safety scope

## Recommended Workflow

### 01_TELEGRAM_TRIGGER
Input: Russian text, voice, URL, or image.

### 02_ROUTE_CLASSIFIER
Classifies intent:
- create listing draft
- improve photos
- generate title
- generate HTML
- review current draft
- stop
- cleanup audit

### 03_AGENT_DISPATCH
Calls the correct controlled agent.

### 04_ARTIFACT_COLLECTOR
Collects photos, title, specifics, HTML, critic report.

### 05_TELEGRAM_PREVIEW
Sends preview to operator.

### 06_APPROVAL_GATE
Records approve/reject/rework.

### 07_RUNNER_HANDOFF
Only if gate allows.

## Live Action Requirements
Before live action n8n may hand off to runner only if:
- Product Passport PASS
- Evidence Map PASS
- Marketplace Critic PASS
- Telegram approval exists
- exact payload exists
- protected fields verified
- token guard path verified
- readonly before-state exists

## Cleanup Requirements
Before cleanup n8n may hand off only if:
- readonly audit exists
- file classification exists
- archive exists
- archive hash verified
- cleanup manifest exists
- explicit operator approval exists

## Stop Conditions
- missing state
- missing next_allowed_action
- critic not PASS
- Telegram approval missing
- protected field mismatch
- live scope unclear

## Next Implementation Layer
Create local/Windows sandbox workflow first. Server n8n or server bridge only after cleanup audit and deployment plan.
