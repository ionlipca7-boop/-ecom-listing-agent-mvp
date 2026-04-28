# 20_FINAL_MODULE_MAP_V1

Status: FINAL_DRAFT_FOR_REVIEW
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Convert the architecture audit into a realistic final module map for first implementation planning.

## System identity
ECOM OS is a modular, operator-governed, multi-marketplace commerce control system.
First practical target: stable eBay workflow.
Future targets: Amazon, other marketplaces, agents, n8n, finance connector, advanced analytics.

---

# CORE MVP MODULES

## 00_brain_orchestrator
Role:
- Single control brain.
- Reads current state / pointer.
- Enforces next_allowed_action.
- Routes work to modules.
- Blocks unsafe live actions.

Owns:
- route control
- safety gate checks
- environment decision
- module dispatch

Must not own:
- marketplace-specific payload details
- secrets
- direct Telegram UI text

Priority: P0
Risk: High

---

## 01_telegram_ru_operator_layer
Role:
- Russian operator control panel.
- Text/voice-ready conversational control.
- Approval buttons and status messages.

Owns:
- Russian user messages
- operator intents
- Telegram approvals
- notifications

Must not:
- publish directly
- revise/delete directly
- bypass Brain

Priority: P0
Risk: Medium

---

## 02_universal_product_model
Role:
- Neutral product/listing data model before marketplace payloads.

Owns:
- supplier data
- stock references
- product facts
- German content
- media list
- variants/bundles
- marketplace payload slots
- approval/verification state

Priority: P0
Risk: High

---

## 03_inventory_sales_core
Role:
- Single source of truth for stock, purchase data, sales, reservations, bundles.

Owns:
- quantity_total
- quantity_available
- quantity_reserved
- quantity_sold
- supplier purchase information
- bundle component deduction
- oversell protection

Must not:
- let marketplaces own stock truth
- change live marketplace quantity without Brain path

Priority: P0
Risk: High

---

## 04_listing_quality_engine
Role:
- Score draft listing quality before approval.

Owns:
- title score
- description score
- HTML score
- photo score
- compliance score
- price/margin score
- AI-search readiness score

Priority: P0
Risk: Medium

---

## 05_marketplace_validation_engine
Role:
- Validate marketplace-specific requirements before payload/live action.

Owns:
- eBay category/item specifics checks
- variation support checks
- image rules checks
- Amazon schema validation in future

Priority: P0
Risk: High

---

## 06_ebay_adapter
Role:
- First live marketplace adapter.

Owns:
- eBay read-only checks
- create offer path
- publish offer path after approval
- real active visibility verify
- eBay offers/promotions future capability

Must not:
- treat API success as final business success
- bypass verify after publish

Priority: P0
Risk: High

---

## 07_approval_gate
Role:
- Operator approval for draft/publish/revise/delete/ads/offers.

Owns:
- approval records
- allowed actions
- high-risk action gates

Priority: P0
Risk: High

---

## 08_recovery_playbooks
Role:
- Safe procedures for known failures.

Owns:
- token failure playbook
- 504 timeout playbook
- missing visibility after API success
- server/local mismatch
- inventory sync mismatch

Priority: P0
Risk: Medium

---

## 09_archive_memory_audit
Role:
- Keep history, transitions, decisions, audit logs.

Owns:
- transition files
- ADRs
- error history
- listing lifecycle history

Must not:
- replace current pointer as current truth

Priority: P0
Risk: Medium

---

# P1 BUSINESS INTELLIGENCE MODULES

## 10_competitor_price_intelligence
Role:
- Research market, competitors, top sellers, price range, title/photo patterns.

Priority: P1
Risk: Medium

## 11_variant_bundle_engine
Role:
- Decide single vs multi-quantity vs variation vs bundle/kit.

Priority: P1
Risk: Medium-High

## 12_ads_offers_strategy
Role:
- Recommend eBay offers to watchers, promoted listing ad rate, ROI/margin guard.

Priority: P1
Risk: Medium-High

## 13_performance_feedback_loop
Role:
- Track impressions, CTR, watchers, sales velocity, stale listings, ad ROI.

Priority: P1
Risk: Medium

---

# P2 EXPANSION MODULES

## 14_amazon_adapter_future
Role:
- Future Amazon SP-API adapter with product type schema validation.

Priority: P2
Risk: High

## 15_finance_connector
Role:
- Export sales, purchases, fees, receipt metadata to separate finance/tax system.

Priority: P2
Risk: Medium

## 16_ai_search_content_engine
Role:
- AEO/GEO/AI-search-ready facts, buyer questions, compatibility, use cases.

Priority: P2
Risk: Medium

---

# P3 FUTURE AUTOMATION MODULES

## 17_n8n_orchestration_future
Role:
- External workflow orchestration after core is stable.

Priority: P3
Risk: High

## 18_agent_runner_future
Role:
- Specialized agents: listing, photo, price, competitor, validator, archivist, runner.

Priority: P3
Risk: High

## 19_predictive_analytics_future
Role:
- Forecast demand, stale risk, supplier quality, seasonality.

Priority: P3
Risk: Medium-High

---

# Required communication flow

```text
Telegram / Operator
  -> Telegram RU Operator Layer
  -> Brain Orchestrator
  -> State / Rules / Approval Gate
  -> Target Module
  -> Verification
  -> Archive / Audit
  -> Telegram response in Russian
```

Forbidden:
- Telegram -> eBay direct publish
- Listing Builder -> marketplace direct publish
- Ads strategy -> live ads without approval
- Inventory -> marketplace live change without Brain path
- GitHub audit -> server runtime

---

# First implementation order

1. Brain Orchestrator hard gate
2. Universal Product Model
3. Inventory Sales Core
4. Telegram RU operator layer
5. Quality Score System
6. Marketplace Validation Engine
7. eBay Adapter real visibility verify
8. Approval Gate integration
9. Recovery Playbooks
10. Archive/Memory/Audit stabilization

---

# Finish condition for architecture phase
Architecture phase is complete when:
- FINAL_MODULE_MAP exists
- CORE_VS_FUTURE_MATRIX exists
- MVP_EXECUTION_ORDER exists
- IMPLEMENTATION_ROADMAP exists
- operator reviews and approves transition to implementation planning

STOP: This file is a plan only. No runtime changes.
