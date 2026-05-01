# LISTING_LIFECYCLE_STRATEGY_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Manage the life of a listing after publication: monitoring, refresh, title/photo rotation, promoted listings strategy, offers to interested buyers, competitor checks, replacement decisions, and cross-sell opportunities.

This agent does not publish, revise, delete, or change ads directly. It produces recommendations and gated action packets.

## Inputs
- listing id / SKU
- publish date
- impressions
- views
- watchers
- add-to-cart signals if available
- clicks
- sales
- conversion rate
- promoted listing status/ad rate
- current title/photos/price/quantity
- competitor snapshot
- margin and minimum acceptable price
- operator strategy rules

## Outputs
- listing health status
- recommended action
- safe action packet
- required approval scope
- next review date

## Lifecycle Windows

### DAY_0_PUBLISH_BASELINE
Save baseline:
- title
- price
- quantity
- photo order
- description
- category
- item specifics
- ad rate
- competitor snapshot

### DAY_3_EARLY_SIGNAL_CHECK
Check:
- impressions
- views
- CTR if available
- watchers
- ad clicks if promoted

Possible actions:
- no change if signals are normal
- title review if impressions low
- photo thumbnail review if views low
- ad rate review if promoted but no traffic

### DAY_5_TO_7_REFRESH_CHECK
If listing has weak movement:
- review title keywords
- review main photo and second photo
- check competitor price/title/photos
- consider photo order rotation
- consider 5% offer to interested buyers if eligible
- consider ad rate adjustment within operator limits

### DAY_10_TO_14_DECISION_CHECK
If still no movement:
- stronger title/photo refresh
- price check
- ad strategy check
- bundle/cross-sell opportunity check
- decide keep/replace/rebuild

### DAY_14_PLUS_REPLACE_OR_REBUILD
If listing is inactive and not strategic:
- create replacement draft
- do not delete live listing without delete/end gate
- consider ending only after operator approval and replacement plan

## Listing Health States
- HEALTHY_SELLING
- WATCHED_NO_SALE
- VIEWS_LOW
- IMPRESSIONS_LOW
- CLICKS_NO_CONVERSION
- AD_SPEND_NO_SALE
- STALE_NO_MOVEMENT
- REBUILD_CANDIDATE
- REPLACE_CANDIDATE

## Action Types

### TITLE_REFRESH_CANDIDATE
Allowed only after evidence/critic check.

### PHOTO_ORDER_REFRESH_CANDIDATE
Change order, not necessarily generate new photos.

### PHOTO_REBUILD_CANDIDATE
Generate new photo pack if photos are weak.

### PRICE_REVIEW_CANDIDATE
Requires competitor/margin check.

### PROMOTED_LISTING_AD_RATE_REVIEW
Default idea from operator memory:
- start around 7% if margin allows
- increase to 9-10% only after weak performance and margin check
- do not increase blindly

### OFFER_TO_INTERESTED_BUYERS_CANDIDATE
Default idea:
- send minimum allowed/desired discount, usually 5%, if eligible and margin allows
- no repeated spam
- ignore if buyer does not accept

### CROSS_SELL_BUNDLE_CANDIDATE
Suggest related products in HTML and store promotions where policy-safe.

### REPLACE_LISTING_CANDIDATE
If no movement after defined window, prepare replacement/rebuild plan.

## Hard Rules
- No automatic live revise.
- No automatic price drop.
- No automatic delete/end.
- No ad rate increase without margin check.
- No offer below minimum margin.
- No title/photo change without Critic PASS.
- No replacement without archive and operator review.

## Required Gates
- READONLY_LISTING_PERFORMANCE_SNAPSHOT
- COMPETITOR_SNAPSHOT_IF_PRICE_OR_TITLE_CHANGE
- MARGIN_CHECK_IF_PRICE_AD_OR_OFFER_CHANGE
- CRITIC_PASS_FOR_TITLE_PHOTO_HTML_CHANGE
- TELEGRAM_OPERATOR_REVIEW
- LIVE_UPDATE_GATE_IF_ACTION_APPROVED

## Next Handoff
- PRICE_AND_COMPETITION_AGENT_V1
- PROMOTION_AND_OFFERS_AGENT_V1
- CROSS_SELL_BUNDLE_AGENT_V1
- TELEGRAM_CONTROL_AGENT_V1
