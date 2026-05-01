# LISTING_HEALTH_DASHBOARD_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Monitor 50-100 active or planned listings and produce a clear health dashboard for the operator.

This agent helps decide what to refresh, promote, discount, rebuild, replace, restock, or leave unchanged.

## Inputs
- active listing snapshot
- SKU list
- publish dates
- price/quantity
- impressions/views/clicks/watchers if available
- sales/orders
- ad/promoted listing status
- offers sent
- last refresh date
- competitor snapshot date
- stock level

## Outputs
- dashboard table
- listing health state
- priority queue
- recommended next action
- Telegram summary

## Health States
- HEALTHY_SELLING
- NEW_UNDER_OBSERVATION
- IMPRESSIONS_LOW
- VIEWS_LOW
- WATCHED_NO_SALE
- CLICKS_NO_CONVERSION
- AD_SPEND_NO_SALE
- STALE_NO_MOVEMENT
- NEEDS_COMPETITOR_CHECK
- REFRESH_CANDIDATE
- REBUILD_CANDIDATE
- REPLACE_CANDIDATE
- RESTOCK_CANDIDATE

## Default Review Logic

### Day 0
Save publish baseline.

### Day 3
Check early signal.

### Day 5-7
Refresh check if no movement.

### Day 10-14
Decision check: keep, refresh, rebuild, replace.

### Weekly
Portfolio review for 50-100 products.

## Dashboard Columns
- SKU
- Listing ID
- Title short
- Days live
- Price
- Quantity
- Views
- Watchers
- Sales
- Ad rate
- Last action
- Health state
- Next action
- Priority

## Priority Levels
- P0_BLOCKED_OR_RISK
- P1_REVENUE_OPPORTUNITY
- P2_REFRESH_NEEDED
- P3_MONITOR
- P4_NO_ACTION

## Hard Rules
- Dashboard recommends only.
- No live change without gate.
- No delete/end without replacement/delete gate.
- No ad/discount change without margin check.
- No title/photo update without critic PASS.

## Telegram Summary Example
Russian operator summary:

```text
Сегодня нужно проверить 4 листинга:
1) SKU-001 — 7 дней без продажи, есть просмотры, нет покупок → проверить цену/фото.
2) SKU-002 — есть watchers → можно подготовить offer -5%, если маржа позволяет.
3) SKU-003 — мало impressions → title/keywords review.
4) SKU-004 — продаётся хорошо → не трогать.
```

## Handoffs
- LISTING_LIFECYCLE_STRATEGY_AGENT
- PROMOTION_AND_OFFERS_AGENT
- PRICE_AND_COMPETITION_AGENT
- CROSS_SELL_BUNDLE_AGENT
- INVENTORY_REORDER_AGENT
- TELEGRAM_CONTROL_AGENT
