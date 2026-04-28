# 41_ADS_OFFERS_AND_CONVERSION_OPTIMIZATION_GOVERNANCE_V1

Status: ADS_OFFERS_CONVERSION_GOVERNANCE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define governance for ads, offers, discounts, and conversion optimization in ECOM OS.

This layer helps improve sales without destroying margin, bypassing approval, or creating unsafe marketplace automation.

## External practice alignment
This strategy follows:
- eBay Promoted Listings general/priority campaign concepts;
- eBay fixed/dynamic ad-rate strategy;
- eBay volume pricing and promotions;
- Amazon ACOS/ROAS advertising measurement;
- margin-aware promotion control;
- operator-governed automation.

## Core decision
Ads/Offers layer recommends.
Brain governs.
Operator approves risky or live actions.
Marketplace Adapter executes only after approval and validation.

Forbidden route:

```text
Ads/Offers Engine -> direct live ad/offer action
```

Correct route:

```text
Performance Signals
 -> Ads/Offers Recommendation
 -> Margin Guard
 -> Brain Governance
 -> Operator Approval
 -> Marketplace Adapter
 -> Verify Result
```

## Supported optimization types
- offer to interested buyers / watchers;
- promoted listing recommendation;
- ad-rate recommendation;
- volume pricing recommendation;
- markdown/promotion recommendation;
- bundle promotion recommendation;
- stale inventory discount recommendation;
- ad pause / reduce recommendation.

## Signal inputs
The layer may consume:
- impressions;
- views;
- CTR;
- watchers/interested buyers;
- add-to-cart signals if available;
- sales velocity;
- stale days;
- competitor price range;
- inventory pressure;
- margin data;
- ad spend;
- ad revenue;
- marketplace fee estimate;
- return risk.

## Margin guard
No ad/offer recommendation may proceed if expected profit falls below minimum margin.

Required calculations:
- purchase cost;
- shipping cost;
- marketplace fee;
- ad cost;
- discount cost;
- return risk buffer;
- minimum profit.

## eBay governance
Possible eBay actions:
- Promoted Listings general strategy;
- fixed ad-rate recommendation;
- dynamic ad-rate recommendation;
- volume pricing recommendation;
- send offer recommendation;
- markdown promotion recommendation.

Rules:
- offer default can start from conservative discounts such as 5% when margin allows;
- ad-rate recommendations must consider margin;
- dynamic ad rate may be recommended but not auto-enabled without approval;
- volume pricing requires sufficient inventory;
- promotions require stock and margin checks.

## Amazon governance future
Amazon advertising should use:
- ACOS;
- ROAS;
- campaign spend;
- ad revenue;
- product margin;
- inventory availability.

Amazon ads remain future until stable eBay core exists.

## Recommendation schema

```json
{
  "recommendation_type": "offer | ad_rate | volume_pricing | markdown | pause_ads",
  "marketplace": "ebay",
  "target_listing_id": "",
  "confidence": 0,
  "expected_margin_after_action": 0,
  "risk_notes": [],
  "requires_operator_approval": true,
  "requires_verification": true
}
```

## Automation boundaries
Allowed without live execution:
- analysis;
- recommendation;
- simulation;
- draft promotion plan;
- operator notification.

Requires approval:
- sending offers;
- enabling ads;
- changing ad rate;
- starting promotion;
- applying volume pricing;
- price changes.

## Anti-loss rules
Stop if:
- margin guard fails;
- inventory is too low;
- product is already selling well without ads;
- ad cost would exceed expected profit;
- stale data is used;
- marketplace verification route is missing;
- operator approval is missing.

## Conversion strategy examples

### Watchers but no sales
Recommendation:
- offer 5% discount if margin allows;
- improve title/photos if CTR is low;
- review competitor price.

### High impressions but low CTR
Recommendation:
- improve hero image;
- improve title;
- review price position.

### High CTR but no sales
Recommendation:
- review price;
- improve description;
- add compatibility/use-case clarity;
- consider small offer.

### Strong organic sales
Recommendation:
- reduce or pause ads;
- protect margin;
- increase stock if supplier reliable.

## Verification ownership
Adapter verifies marketplace result.
Brain requires verification before route advancement.

Examples:
- ad status verify;
- offer delivery verify;
- promotion status verify;
- margin result audit.

## STOP conditions
STOP if:
- automation tries to send live offer without approval;
- ads are enabled automatically without approval;
- margin guard missing;
- inventory data missing;
- ad cost can exceed profit;
- marketplace adapter verification missing;
- recommendation copies competitor text;
- operator override is ignored.

STOP: This document defines ads/offers/conversion governance only. It does not execute ads, offers, discounts, price changes, or live marketplace actions.
