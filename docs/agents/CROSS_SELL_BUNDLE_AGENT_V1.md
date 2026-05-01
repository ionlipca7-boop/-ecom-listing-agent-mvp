# CROSS_SELL_BUNDLE_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Suggest safe cross-sell, bundle, and related-product links for listings and HTML descriptions.

Goal: help buyers discover compatible products in the seller inventory and increase basket size.

## Inputs
- current product SKU/listing id
- seller inventory/product catalog
- active listing URLs
- category
- compatibility evidence
- price and margin data
- stock quantity if available
- marketplace policy constraints

## Outputs
- related product suggestions
- bundle candidate
- German HTML related-products block
- Telegram review packet

## Use Cases

### Related Products In HTML
Add a clean section such as:
- "Passt gut dazu"
- "Weitere passende Artikel"
- "Auch interessant"

Each link must point to real active seller listings only.

### Bundle Candidate
Suggest compatible combinations:
- cable + adapter
- charger + cable
- adapter set + compatible cable
- phone stand cable + charger
- USB tester + compatible cable/power supply

### Store Navigation
If seller has 50-100 products, create structured related-product recommendations per listing.

## Hard Rules
- No fake compatibility.
- No link to non-existing listing.
- No misleading bundle claim.
- No external unsafe links in description unless marketplace policy allows.
- Use active marketplace listing URLs only.
- Telegram review required before adding cross-sell blocks.
- Do not change live HTML without critic PASS and approval gate.

## Required Evidence
- product category match
- connector/compatibility match
- active listing exists
- price known
- stock known if available

## HTML Block Draft
German-only for eBay Germany:

```html
<section class="related-products">
  <h2>Passt gut dazu</h2>
  <ul>
    <li><a href="LISTING_URL">USB-C Ladegerät passend zu diesem Kabel</a></li>
    <li><a href="LISTING_URL">USB-C Adapter-Set für weitere Anschlüsse</a></li>
  </ul>
</section>
```

## Telegram Packet Must Show
- current product
- related product candidates
- reason why they fit
- active listing URLs
- stock/price if available
- approve/reject options

## Handoffs
- HTML_DESCRIPTION_AGENT
- ITEM_SPECIFICS_AGENT
- PRICE_AND_COMPETITION_AGENT
- TELEGRAM_CONTROL_AGENT
- MARKETPLACE_CRITIC_AGENT
- RUNNER_AGENT only after approval

## Stop Conditions
- active listing URL missing
- compatibility unclear
- related product out of stock
- external link policy unclear
- operator approval missing
