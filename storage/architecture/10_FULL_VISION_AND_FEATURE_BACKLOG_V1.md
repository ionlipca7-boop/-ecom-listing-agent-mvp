# 10_FULL_VISION_AND_FEATURE_BACKLOG_V1

Status: DRAFT_MASTER_BACKLOG
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Project identity
ECOM OS is not only an eBay listing generator. It is a controlled multi-marketplace commerce operating system with Telegram control, AI-assisted listing generation, photo quality control, pricing intelligence, competitor research, approval gates, runtime verification, archive memory, and future marketplace adapters such as Amazon.

## Original and recurring project ideas to preserve

### 1. Telegram Control Room
- Telegram as operator panel.
- Draft preview.
- Approve/fix/reject buttons.
- Publish approval.
- Listing status notifications.
- Error notifications.
- Future dashboard: quality score, price score, risk score, marketplace readiness.

### 2. Brain / Orchestrator
- Single control layer.
- Reads pointer/current state.
- Decides next_allowed_action.
- Routes tasks to blocks.
- Blocks live actions without approval.
- Prevents local/server/GitHub confusion.

### 3. Universal Listing Builder
- German-first listing generation.
- SEO title variants.
- Clean German description.
- Mobile-friendly HTML.
- Structured sections: product, condition, benefits, specs, shipping, notes.
- No garbage text.
- No false claims.
- Marketplace-neutral product model first, then eBay/Amazon payloads.

### 4. HTML / Template Engine
- eBay mobile-friendly HTML.
- Simple responsive layout.
- No risky scripts.
- Marketplace-specific templates.
- German buyer-focused copy.
- Future: template A/B variants.

### 5. Photo / Image Engine
- Automatic photo detection.
- Count photos.
- Validate resolution.
- Detect bad quality, watermarks, foreign-language text, logos, overlays.
- Create eBay-ready image package.
- Future: background cleanup, crop, sequence order, hero image selection.
- Marketplace-specific image rules.

### 6. Price Intelligence
- Competitor price scan.
- Target price.
- Minimum acceptable price.
- Aggressive test price.
- Offer strategy.
- Price refresh after inactivity.
- Store price decision history.

### 7. Market and Competitor Research
- Search active competitors.
- Search sold/completed items where available.
- Detect top sellers.
- Identify best-performing title patterns.
- Compare photo quality.
- Compare shipping/returns.
- Extract market demand signals.
- Recommend category and item specifics.

### 8. eBay Adapter
- Inventory read-only.
- Draft/create offer.
- Publish only with approval.
- Verify after publish with real active listing visibility.
- Use eBay taxonomy/item specifics/category logic.
- Store API response separately from real marketplace visibility.

### 9. Amazon Adapter (future)
- Amazon SP-API support later.
- Product Type Definitions API for required attributes/schemas.
- Listings Items API for listing operations.
- Catalog Items API for ASIN/catalog research.
- Amazon-specific validation before submit.
- No Amazon live path until eBay is stable.

### 10. Marketplace Adapter Layer
- eBay now.
- Amazon later.
- Other marketplaces later: Kaufland, Etsy, Shopify/own store, Kleinanzeigen helper workflow.
- Each marketplace gets its own adapter, validator, publish/verify path.
- No direct marketplace access without Brain + Approval.

### 11. Approval Gate
- Draft approval.
- Publish approval.
- Revise approval.
- Delete approval with extra safety gate.
- Marketplace-specific approval records.

### 12. Strategy Engine
- Refresh listing after 5-7 days inactivity.
- Replace/rework after 14 days if stale.
- Daily listing plan.
- Prioritize best opportunities.
- Never auto-delete.

### 13. Inventory System
- Track active listings.
- Track draft listings.
- Track product source.
- Track listing lifecycle.
- Prevent duplicate listing mistakes.

### 14. Archive / Memory / Audit
- Store transitions.
- Store decisions.
- Store errors and fixes.
- Store per-listing timeline.
- Prevent losing context between chats.

### 15. Recovery Playbooks
- Token failure.
- 504 / gateway timeout.
- Missing active listing after API success.
- Server path mismatch.
- Local vs server command mismatch.
- GitHub sync mismatch.

### 16. Agents and n8n
- n8n for orchestration only after core blocks are stable.
- Agents can be specialized:
  - listing_agent
  - photo_agent
  - price_agent
  - competitor_agent
  - marketplace_validator_agent
  - archivist_agent
  - runner_agent
- Agents must not bypass Brain or Approval Gate.

### 17. GitHub / Server / Local Separation
- GitHub = source and audit.
- Server = runtime and secrets.
- Local Windows = development/history/operator tooling.
- Every action must declare environment.

## New features worth considering

### Listing Quality Score
Score before approval:
- title SEO score
- item specifics completeness
- photo quality score
- price competitiveness score
- description quality score
- marketplace compliance score

### Marketplace Rule Validator
Before creating payload:
- eBay validator
- Amazon validator
- future marketplace validators

### Universal Product Model
Create neutral product object first:
- identity
- attributes
- images
- pricing
- condition
- category candidates
- marketplace payloads
- approval status
- verification status

### Competitor Intelligence Snapshot
For every product draft:
- top competitor titles
- price range
- active/sold signal
- shipping terms
- photo count comparison
- recommended positioning

### Performance Feedback Loop
After listings are active:
- impressions
- clicks
- watchers
- offers
- sales
- stale days
- recommended action

## Implementation priority
P0 Safety:
- Brain hard gate
- real visibility verify
- environment guard
- secrets guard

P1 Listing quality:
- universal listing model
- quality score
- marketplace validators
- German HTML template
- photo gate

P2 Business intelligence:
- competitor research
- price intelligence
- category/item specifics research

P3 Automation:
- Telegram dashboard
- refresh/replace engine
- performance feedback

P4 Expansion:
- Amazon adapter
- n8n orchestration
- specialized agents
- additional marketplaces

## Do not forget
- Project goal: build professional WOW listings, not just publish API payloads.
- Marketplace API success is not enough; real visibility and business performance matter.
- eBay and Amazon rules differ; never hardcode the entire system around one marketplace.
- All live actions require approval.
- Old project must remain preserved.
