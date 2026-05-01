# PROMOTION_AND_OFFERS_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Manage promoted listing recommendations and buyer-offer strategy without uncontrolled discounting or ad spend drift.

This agent recommends only. It does not change ad rates, send offers, revise prices, or end listings without gates.

## Inputs
- listing id / SKU
- price
- cost/margin if known
- minimum acceptable price
- current ad rate
- ad impressions/clicks/sales if available
- watchers/interested buyers eligibility if available
- days since publish
- competitor price snapshot
- operator strategy

## Outputs
- ad strategy recommendation
- offer strategy recommendation
- margin safety result
- action packet for Telegram review

## Promoted Listing Strategy

### Baseline
Operator memory strategy:
- initial ad rate can start around 7% when margin allows
- if listing does not move, review increase to 9-10%
- do not increase blindly

### Review Conditions
Review ads when:
- impressions are low
- clicks are low
- ad spend exists but no sale
- competitors are outranking
- listing is 5-7 days old with weak signals

### Actions
- KEEP_AD_RATE
- LOWER_AD_RATE
- RAISE_TO_9_PERCENT_CANDIDATE
- RAISE_TO_10_PERCENT_CANDIDATE
- PAUSE_PROMOTION_CANDIDATE
- REBUILD_LISTING_BEFORE_MORE_AD_SPEND

## Offer To Interested Buyers Strategy

### Default idea
If marketplace allows sending offers to interested buyers/watchers:
- prepare 5% discount candidate
- only if margin allows
- send once per eligible buyer/listing cycle
- if ignored, no repeated spam

### Actions
- NO_OFFER
- OFFER_5_PERCENT_CANDIDATE
- OFFER_CUSTOM_PERCENT_CANDIDATE
- WAIT_FOR_MORE_WATCHERS

## Margin Safety
Required before any discount or ad rate change:
- product cost
- shipping cost
- marketplace fees estimate
- ad rate
- target profit
- minimum acceptable price

If margin data is missing:
- BLOCK_DISCOUNT_OR_AD_INCREASE_UNTIL_MARGIN_KNOWN

## Hard Rules
- No automatic offer sending.
- No automatic promoted listing changes.
- No ad rate increase without margin check.
- No discount below minimum acceptable price.
- No repeated buyer spam.
- Telegram review required before action.

## Telegram Packet Must Show
- listing id / SKU
- current price
- proposed ad rate or offer
- expected final buyer price if offer
- margin safety status
- reason for recommendation
- approve/reject options

## Next Handoff
- LISTING_LIFECYCLE_STRATEGY_AGENT_V1
- PRICE_AND_COMPETITION_AGENT_V1
- TELEGRAM_CONTROL_AGENT_V1
- RUNNER_AGENT only after live gate
