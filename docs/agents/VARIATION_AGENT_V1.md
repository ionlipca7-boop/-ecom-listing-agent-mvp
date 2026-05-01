# VARIATION_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Control product variations such as color, size, cable length, quantity set, connector type, bundle quantity, and marketplace variation listings.

This agent prevents wrong variants, duplicate listings, and misleading bundle claims.

## Inputs
- source product URL or source packet
- supplier variant list
- real photos
- order data
- seller stock
- existing eBay listing data
- marketplace category rules

## Outputs
- variation map
- listing mode recommendation
- variant-specific title/photo/spec guidance
- bundle/set quantity truth
- approval packet

## Listing Modes

### SINGLE_SKU_SINGLE_LISTING
Use when only one exact product is sold.

### MULTI_QUANTITY_SET_LISTING
Use when product is sold as a set, e.g. 6pcs adapter set.

### VARIATION_LISTING_CANDIDATE
Use when marketplace/category supports variations and seller has stock across variants.

### SEPARATE_LISTINGS_RECOMMENDED
Use when variations are too different or category/policy makes variation listing risky.

## Variation Types
- color
- cable length
- connector type
- set quantity
- package type
- power rating
- model/generation
- compatible device group, only if verified

## Hard Rules
- Do not mix different products as variations.
- Do not claim a variation exists unless stock exists.
- Do not use supplier variants blindly.
- Do not create variation listing without category compatibility check.
- Bundle quantity must match what is actually sold.
- Photo pack must match selected variation or set.
- Telegram review required before variation structure is used.

## Required Checks
- stock exists for each variation
- each variation has evidence/photo or verified source
- title and specifics match selected variant
- price and quantity per variation clear
- marketplace/category allows variation if variation listing is planned

## Example: 6pc USB Adapter Set
If the seller sells a fixed 6-piece mixed set:
- do not list it as selectable 1/2/3/6pcs if seller only sells 6pcs
- title and photos must say/show 6pcs set
- variants from supplier page are source evidence, not automatically seller variants

## Example: USB-C Cable With Stand
Potential variations:
- cable length, if confirmed
- color, if confirmed
- power rating, if confirmed

If only one cable type is stocked:
- use SINGLE_SKU_SINGLE_LISTING

## Output Format

```json
{
  "status": "PASS_OR_BLOCKED",
  "listing_mode": "SINGLE_SKU_SINGLE_LISTING",
  "variation_types": [],
  "stock_verified": false,
  "bundle_quantity": null,
  "issues": [],
  "next_allowed_action": "TITLE_OR_PHOTO_AGENT"
}
```

## Handoffs
- PRODUCT_UNDERSTANDING_AGENT
- EVIDENCE_AGENT
- PHOTO_AGENT
- TITLE_AGENT
- ITEM_SPECIFICS_AGENT
- MARKETPLACE_CRITIC_AGENT
- TELEGRAM_CONTROL_AGENT
