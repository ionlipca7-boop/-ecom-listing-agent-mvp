# ECOM_OS_V3_PROJECT_AGENT_MAP_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Map the full ECOM OS V3 agent system, current proof state, missing parts, and safe implementation order.

## Canonical Base
Existing project canon:

1. manifest
2. rules
3. state
4. history
5. control_agent
6. archivist_agent
7. runner_agent
8. n8n_orchestration
9. compact_core_migration

New marketplace listing layer must extend this canon without replacing it.

## Current Overall Progress Estimate

### Design / Canon
Approximate status: 70%+

Completed design docs:
- MARKETPLACE_VISUAL_LISTING_AGENT_V1
- MARKETPLACE_VISUAL_LISTING_AGENT_V1.schema.json
- SERVER_RUNTIME_CLEANUP_DISCIPLINE_V1
- ECOM_OS_V3_VISUAL_AGENT_AUDIT_POINTER_V1
- LISTING_AGENT_PIPELINE_V1
- URL_INTAKE_AGENT_V1
- TELEGRAM_CONTROL_AGENT_V1
- MARKETPLACE_CRITIC_AGENT_V1
- N8N_ORCHESTRATION_HANDOFF_V1
- SERVER_CLEANUP_AUDIT_PLAN_V1
- TEACHER_AGENT_LEARNING_MEMORY_V1

### Visual Sandbox Proof
Approximate status: 60%+

Confirmed:
- photo pack proof for real 6-piece adapter product
- photo pack proof for USB-C cable with foldable phone stand
- German infographic proof
- title visual proof
- item specifics visual proof
- HTML preview proof

Still missing:
- local executable harness
- saved artifacts in project format
- repeatable tests across 2-3 products

### URL Intake Automation
Approximate status: 25%

Confirmed:
- URL failure pattern identified for AliExpress/Alibaba short links
- screenshot fallback works manually

Missing:
- link resolver
- browser extraction
- screenshot parser
- image extractor
- structured source packet writer

### Telegram Control
Approximate status: 30%

Confirmed:
- Telegram runtime exists in project/server memory
- desired commands and safety rules documented

Missing:
- Russian voice transcription route
- photo upload intake route
- URL intake command route
- visual preview packet sender
- approve/reject/rework buttons or command parser
- critic report display

### n8n Orchestration
Approximate status: 35%

Confirmed:
- n8n role documented as orchestration only
- handoff rules documented

Missing:
- executable workflow update
- state handoff schema
- agent dispatch nodes
- Telegram preview path

### Server Runtime
Approximate status: unknown until audit

Known memory:
- server path: /home/ionlipca7/runtime_eco_v1
- Telegram/eBay/EPS/token guard existed or were used in previous work
- production server may contain V3/V4/V5 temporary files

Missing:
- readonly runtime pollution audit
- current pointer verify
- protected file list verify
- cleanup manifest
- implementation deploy plan

## Agent Map

### CONTROL_AGENT
Role: enforce route, gates, next_allowed_action.
Status: existing canon base.
Needs: updated pointer to ECOM OS V3 listing pipeline after local tests.

### ARCHIVIST_AGENT
Role: archive inputs, outputs, proofs, decisions, lessons.
Status: existing canon base.
Needs: artifact format for photo/title/specifics/HTML/critic/Telegram proof.

### RUNNER_AGENT
Role: execute only gated actions.
Status: existing canon base.
Needs: new safe runner commands for local sandbox, readonly audit, dry-run, live gate.

### URL_INTAKE_AGENT
Role: URL/screenshot/photo source intake.
Status: design created, weak automation.
Priority: high.

### PRODUCT_UNDERSTANDING_AGENT
Role: Product Passport.
Status: included in visual-agent design.
Priority: high.

### EVIDENCE_AGENT
Role: claim-to-evidence map.
Status: included in visual-agent design.
Priority: high.

### MARKETPLACE_RULES_AGENT
Role: load eBay Germany rules, photo/text/language constraints.
Status: included in visual-agent design.
Priority: high.

### PHOTO_AGENT
Role: create 8-12 image pack.
Status: sandbox proof visually good.
Priority: high.

### TITLE_AGENT
Role: German title options and recommended title.
Status: sandbox proof visually good.
Priority: medium-high.

### ITEM_SPECIFICS_AGENT
Role: German article specifics.
Status: sandbox proof visually good.
Priority: medium-high.

### HTML_DESCRIPTION_AGENT
Role: German HTML description and preview.
Status: sandbox proof visually good.
Priority: medium-high.

### PRICE_AND_COMPETITION_AGENT
Role: price range, competitor comparison, margin logic.
Status: not yet implemented in new V3 pipeline.
Priority: medium.
Rule: must use current web/marketplace data when recommending price.

### MARKETPLACE_CRITIC_AGENT
Role: mandatory quality/safety gate.
Status: design created.
Priority: critical.

### TELEGRAM_CONTROL_AGENT
Role: Russian operator interface.
Status: design created.
Priority: critical.

### TEACHER_AGENT
Role: learn from feedback, failures, successes, critic blocks, operator preferences.
Status: design created.
Priority: high.

### CLEANUP_ARCHIVIST_AGENT
Role: cleanup route after readonly audit.
Status: design created.
Priority: high before server deployment.

### N8N_ORCHESTRATION_HANDOFF
Role: dispatch and state handoff only.
Status: design created.
Priority: medium-high after local tests.

## Recommended Next Route

### A. GitHub design registration
Status: done for current docs.

### B. Windows local sandbox integration
Next.
Build local runner that can create project artifacts without server.

### C. Two-product repeatability test
Use:
1. USB-C cable with foldable stand
2. 6-piece USB adapter set

Required output per product:
- source packet
- Product Passport
- Evidence Map
- 8-image gallery/contact sheet
- title candidates
- item specifics
- HTML preview
- critic report
- archive package

### D. Server readonly cleanup audit
No delete.

### E. Telegram control sandbox
Telegram accepts URL/photo/voice and returns preview.

### F. n8n handoff integration
Controlled orchestration only.

### G. Server deployment plan
Only after cleanup audit and local sandbox PASS.

### H. eBay dry-run
No live update until exact live gate.

### I. Live marketplace update/create route
Only after approval, token guard, readonly before/after verify.

## Current Next Allowed Action
`WINDOWS_LOCAL_SANDBOX_INTEGRATION_PLAN_V1`

## Stop Rule
Do not move to server until local sandbox and readonly cleanup audit are complete.
