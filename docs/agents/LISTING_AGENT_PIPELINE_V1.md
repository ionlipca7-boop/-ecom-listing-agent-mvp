# LISTING_AGENT_PIPELINE_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Define the complete controlled listing pipeline after the successful sandbox proofs for photo, title, item specifics, and HTML preview.

This document extends the existing ECOM CONTROL ROOM canon:

1. manifest
2. rules
3. state
4. history
5. control_agent
6. archivist_agent
7. runner_agent
8. n8n_orchestration
9. compact_core_migration

It does not replace the control layer. It adds a marketplace listing pipeline governed by A -> B -> FINISH -> STOP.

## Current Proof Status

### Confirmed sandbox proofs
- PHOTO_AGENT: PASS for real-product visual photo pack proof.
- TITLE_AGENT: PASS for German title suggestions preview.
- ITEM_SPECIFICS_AGENT: PASS for German item specifics preview.
- HTML_AGENT: PASS for German HTML description preview.

### Not production-ready yet
- URL_INTAKE_AGENT is weak for AliExpress/Alibaba short/mobile/share links.
- TELEGRAM_CONTROL_AGENT is not yet complete.
- CRITIC_AGENT must become mandatory before any Telegram/live step.
- SERVER_CLEANUP_AUDIT must happen before production integration.

## Pipeline Order

### 01_URL_INTAKE_AGENT
Input:
- Product URL from AliExpress, Alibaba, Amazon, eBay, or supplier site.
- Optional screenshots if URL is blocked.
- Optional real photos if available.

Output:
- Source intake packet.

Rules:
- Try URL first.
- If URL is blocked, do not hallucinate.
- Ask for minimal fallback: 1-3 screenshots or real photos.
- Preserve source marketplace, title, product images, variants, price, MOQ, and visible claims.

### 02_PRODUCT_UNDERSTANDING_AGENT
Output:
- Product Passport.

Must identify:
- product type
- bundle quantity
- visible features
- connector/type/variant
- color/material
- included items
- uncertainty list

No next step before Product Passport PASS.

### 03_EVIDENCE_AGENT
Output:
- Evidence Map.

Rules:
- Every title/photo/spec/description claim must map to visible source or user-provided evidence.
- Unknown fields must remain unknown or be marked not confirmed.
- No fake measurements, no fake compatibility, no fake brand claims.

### 04_MARKETPLACE_RULES_AGENT
Output:
- Marketplace rule profile.

Default profile for current project:
- marketplace: eBay Germany
- language: German only
- main photo: clean, no text, no watermark, no border
- secondary photos: allowed only if policy-safe and claim-safe
- max image plan: 8-12 by default, up to marketplace limit when needed

### 05_PHOTO_AGENT
Output:
- 8-12 image plan and generated/edited sandbox pack.

Default image structure:
1. clean main photo, no text
2. second clean angle, no text
3. German feature infographic
4. main use case
5. desk/lifestyle use case
6. detail view
7. mechanism/function close-up
8. product overview
9-12 optional: dimensions, package, compatibility, bundle/included items, only if evidence exists

### 06_TITLE_AGENT
Output:
- 3-5 German title candidates
- recommended title
- character count
- SEO keyword reasoning

Rules:
- German only for eBay Germany.
- No unsupported brand/model claims.
- No keyword spam.
- Prefer compact title that starts with exact product type.

### 07_ITEM_SPECIFICS_AGENT
Output:
- marketplace field/value draft.

Rules:
- Use confirmed facts only.
- If brand is unclear, mark neutral/not confirmed.
- Protect existing live listing fields unless update scope approves change.

### 08_HTML_DESCRIPTION_AGENT
Output:
- German HTML description
- mobile-friendly preview
- sections: headline, highlights, technical data, delivery contents, notice

Rules:
- German only.
- Clean HTML.
- No external scripts.
- No fake claims.

### 09_PRICE_AND_COMPETITION_AGENT
Output:
- recommended listing price range
- competitor notes
- margin notes if cost is known

Rules:
- Use web/current marketplace data when price recommendation is needed.
- Do not update live price without explicit scope.

### 10_MARKETPLACE_CRITIC_AGENT
Output:
- PASS/BLOCKED report.

Checks:
- Product Passport PASS
- Evidence Map PASS
- photo 1-2 clean
- German language
- title length/clarity
- item specifics consistency
- HTML consistency
- eBay policy safety
- protected fields preserved

No Telegram approval packet before Critic PASS.

### 11_TELEGRAM_CONTROL_AGENT
Output:
- human review packet
- approve/reject/rework route

Must support:
- Russian operator text
- Russian voice command after transcription
- product URL input
- product photo input
- preview galleries
- title/spec/HTML preview
- approve/reject/rework commands

### 12_N8N_ORCHESTRATION_HANDOFF
Purpose:
Route agent steps into controlled automation.

Allowed n8n role:
- orchestration only
- step dispatch
- state handoff
- notification handoff
- no uncontrolled live action

### 13_RUNNER_AGENT
Purpose:
Execute only gated actions.

Runner may execute:
- sandbox generation
- local validation
- server readonly audit
- eBay dry-run
- live update only after live gate

### 14_ARCHIVIST_AGENT
Purpose:
Save proof and continuity.

Must archive:
- input packet
- source screenshots/photos
- product passport
- evidence map
- photo pack
- title/options
- specifics
- HTML
- critic report
- Telegram approval
- final listing proof

## Required Gates

### GATE_A_INPUT_READY
PASS requires URL or fallback evidence.

### GATE_B_PRODUCT_PASSPORT
No output before product truth is known.

### GATE_C_EVIDENCE_MAP
No unsupported claims.

### GATE_D_PHOTO_PACK_SANDBOX
Visual output must be human-visible.

### GATE_E_LISTING_TEXT_SANDBOX
Title, specifics, HTML must be previewed.

### GATE_F_CRITIC_PASS
No Telegram approval before critic PASS.

### GATE_G_TELEGRAM_OPERATOR_APPROVAL
No server/live change before human approval.

### GATE_H_SERVER_DEPLOY
Only after cleanup audit and implementation plan.

### GATE_I_LIVE_MARKETPLACE_ACTION
Only after token guard, readonly before-state, exact payload, approval, and readonly after-state.

## Stop Conditions
- URL inaccessible and no fallback evidence.
- Product identity unclear.
- Evidence missing.
- Visual pack not shown to operator.
- Critic BLOCKED.
- Telegram approval missing.
- Server cleanup not completed before deployment.
- Live action scope unclear.

## Next Allowed Action
Create companion docs:
- URL_INTAKE_AGENT_V1.md
- TELEGRAM_CONTROL_AGENT_V1.md
- MARKETPLACE_CRITIC_AGENT_V1.md
- N8N_ORCHESTRATION_HANDOFF_V1.md
- SERVER_CLEANUP_AUDIT_PLAN_V1.md
