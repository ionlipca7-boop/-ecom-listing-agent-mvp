# 08_UPGRADE_BACKLOG_V1

Status: DRAFT_PROPOSAL_ONLY
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Purpose
Define possible upgrades for ECOM OS / ECOM LISTING AGENT MVP after architecture audit, without changing runtime behavior yet.

## Upgrade principle
Do not upgrade by rewriting the whole project. Use modular-monolith first, with clear boundaries, safety gates, and incremental replacement of weak paths.

## P0 - Safety and control upgrades
1. Brain Orchestrator Hard Gate
- Single executable decision layer.
- Reads current pointer/state.
- Allows only next_allowed_action.
- Blocks publish/revise/delete unless gate is explicitly open.

2. Real Visibility Verify after Publish
- Publish API success is not enough.
- Add mandatory read-only verification that listing is visible/active on eBay.
- Store result separately from publish response.

3. Environment Guard
- Every command/action must declare environment: GitHub, local Windows, server runtime.
- No mixed shell contexts.
- Server actions require explicit read-only/live gate.

4. Secrets Guard
- Never print or commit secrets.
- Audit branch must not read env/token values.

## P1 - Core business upgrades
1. Listing Quality Scoring
- Score title, description, category, price, images, item specifics before approval.
- Block low-quality listings before Telegram approval.

2. German Listing Template Engine
- Structured German description.
- SEO title variants.
- Condition text.
- Shipping/return/legal sections.

3. Price Intelligence
- Target price, minimum price, aggressive price, fallback price.
- Track price age and refresh windows.

4. Image Quality Gate
- Minimum image count.
- Detect bad/watermarked/foreign-language images.
- Enforce eBay-ready photo package.

## P2 - Automation upgrades
1. Refresh / Replace Strategy
- Refresh after 5-7 days without activity.
- Replace/rework after 14 days if stale.
- Never auto-delete without approval.

2. Telegram Control Dashboard
- Show draft status, quality score, risk score.
- Buttons: approve draft, request fix, approve publish, verify listing.

3. Audit Timeline
- For every listing: draft -> approval -> publish attempt -> verify -> active/stopped.

4. Recovery Playbooks
- Token failure playbook.
- 504 retry playbook.
- Missing listing visibility playbook.
- Server path mismatch playbook.

## P3 - Later upgrades
1. Product Research Block
- Competitor scan.
- Demand signals.
- Category fit.

2. Multi-market support
- Germany first.
- Other markets later only after stable German pipeline.

3. AI Listing Improvement Loop
- Compare active listings performance.
- Improve future templates.

## Rejected for now
- Full rewrite.
- Microservices now.
- Auto-publish without approval.
- Direct Telegram to eBay publish path.
- Server refactor before module map is reviewed.

## Upgrade order
A. Safety guards
B. Module boundaries
C. Telegram dashboard
D. Listing quality scoring
E. eBay real visibility verify
F. Strategy refresh/replace
FINISH. Review before code changes.
STOP. No live action from this document.
