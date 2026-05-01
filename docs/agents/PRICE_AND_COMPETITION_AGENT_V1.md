# PRICE_AND_COMPETITION_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Analyze current market competition, price range, and product opportunity before listing creation or lifecycle changes.

This agent supports product selection, listing pricing, title/photo strategy, and refresh/replacement decisions.

## Inputs
- product URL/source packet
- product cost
- shipping cost
- target marketplace
- competitor URLs/search results
- current listing price if existing
- sales/performance data if existing
- margin target

## Outputs
- competitor snapshot
- recommended price range
- minimum safe price candidate
- opportunity score
- title/photo gaps from competitors
- sourcing reorder suggestion

## Use Cases

### New Product Research
Find what is selling, what competitors show, and whether the product is worth listing.

### Existing Listing Refresh
If a listing has low movement after 5-7 days, compare with competitors:
- price
- title keywords
- main photo quality
- shipping speed
- bundle count
- ad/promotion likely needed

### Replacement Decision
If product/listing is stale, recommend:
- keep
- refresh
- rebuild
- replace with better product

## Required Data
- competitor title
- competitor price
- shipping cost/time if visible
- image quality notes
- bundle/quantity
- sold/market signal if available
- own cost/margin if available

## Hard Rules
- Current web/marketplace data required for live pricing decisions.
- Do not recommend price change without margin and competitor check.
- Do not claim sales volume unless verified.
- Do not copy competitor text/photos directly.
- Do not order new inventory without operator approval.

## Opportunity Score
Score 0-100 based on:
- demand signal
- competition intensity
- own margin
- visual differentiation potential
- shipping feasibility
- listing improvement potential

## Output Format

```json
{
  "status": "PASS_OR_BLOCKED",
  "product": "",
  "marketplace": "ebay_de",
  "competitor_count": 0,
  "recommended_price_range": "",
  "minimum_safe_price": null,
  "opportunity_score": null,
  "recommended_action": "KEEP_REFRESH_REBUILD_REPLACE_ORDER_MORE",
  "evidence": [],
  "next_allowed_action": ""
}
```

## Handoffs
- LISTING_AGENT_PIPELINE_V1
- LISTING_LIFECYCLE_STRATEGY_AGENT_V1
- PROMOTION_AND_OFFERS_AGENT_V1
- PRODUCT_RESEARCH_AGENT_V1
