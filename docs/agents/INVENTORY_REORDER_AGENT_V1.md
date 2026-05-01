# INVENTORY_REORDER_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Help decide what to reorder, what to stop buying, and what new products to test based on listing performance, stock, margin, and market signals.

This agent recommends only. It does not order products automatically.

## Inputs
- SKU inventory
- quantity available
- sales velocity
- product cost
- supplier URL
- supplier price/MOQ/shipping
- marketplace performance
- competitor snapshot
- margin target
- operator budget

## Outputs
- reorder candidate list
- do-not-reorder list
- new product test candidates
- stock risk alerts
- Telegram summary

## Decisions
- REORDER_CANDIDATE
- HOLD_STOCK
- DO_NOT_REORDER
- TEST_SMALL_BATCH
- REPLACE_WITH_BETTER_PRODUCT
- NEEDS_SUPPLIER_CHECK

## Reorder Criteria
Consider reorder when:
- product sells consistently
- margin is acceptable
- supplier price still good
- competition is not too strong
- stock is below threshold

## Stop/Rebuild Criteria
Consider not reordering when:
- stale listing with no movement
- weak margin
- heavy competition
- high return/complaint risk
- source product quality uncertain

## New Product Research
Use with PRICE_AND_COMPETITION_AGENT to identify:
- trending useful accessories
- compatible products with existing catalog
- small low-risk test batches
- bundle opportunities

## Hard Rules
- No automatic purchasing.
- No supplier order without operator approval.
- No product recommendation without cost/margin/market logic.
- Do not trust supplier claims without evidence.

## Telegram Packet
Must show:
- product/SKU
- current stock
- sales signal
- margin signal
- supplier link
- recommendation
- reason
- approve/reject option

## Handoffs
- PRICE_AND_COMPETITION_AGENT
- LISTING_HEALTH_DASHBOARD_AGENT
- CROSS_SELL_BUNDLE_AGENT
- TELEGRAM_CONTROL_AGENT
