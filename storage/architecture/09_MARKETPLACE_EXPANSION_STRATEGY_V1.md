# 09_MARKETPLACE_EXPANSION_STRATEGY_V1

Status: DRAFT_STRATEGY_ONLY
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Strategic requirement
ECOM OS must not be designed as an eBay-only system. eBay is the first live marketplace adapter. Amazon and other marketplaces must be supported later through a common marketplace layer.

## Core decision
Introduce a conceptual `marketplace_adapter_layer` in the architecture plan.

The system should be organized as:

```text
Brain / Orchestrator
  -> Listing Core
  -> Photo Core
  -> Price Core
  -> Approval Gate
  -> Marketplace Adapter Layer
        -> eBay Adapter
        -> Amazon Adapter (future)
        -> Other Marketplace Adapter (future)
  -> Verify Layer
  -> Archive / Audit Layer
```

## Why this matters
If listing logic is built directly around eBay fields, Amazon integration later becomes a rewrite. Instead, we need:

1. Universal internal listing model
2. Marketplace-specific mapping adapters
3. Marketplace-specific validation
4. Marketplace-specific publish/verify paths
5. Shared approval and audit layer

## Universal listing model draft
A future listing should exist first as an internal neutral object:

```json
{
  "product_identity": {},
  "title": {},
  "description": {},
  "images": [],
  "price": {},
  "inventory": {},
  "condition": {},
  "shipping": {},
  "category_suggestions": {},
  "marketplace_payloads": {
    "ebay": {},
    "amazon": {},
    "other": {}
  },
  "approval": {},
  "verification": {}
}
```

## Adapter rules
- No marketplace may bypass Brain.
- No marketplace may bypass Approval Gate.
- No marketplace may directly own the universal listing model.
- Each adapter converts the neutral listing into its own API payload.
- Each adapter must include read-only verification after publish.

## eBay now
- eBay remains the first active adapter.
- eBay-specific files stay in ebay_api_block.
- eBay publish must add real active visibility verification.

## Amazon later
Amazon must be added only after:
- eBay route is stable
- universal listing model exists
- approval gates are marketplace-neutral
- marketplace adapter interface is defined
- secrets/runtime separation is clean

## Future marketplace examples
- Amazon
- Etsy
- Kaufland
- Kleinanzeigen helper workflow
- Shopify or own store later

## Required future blocks
1. marketplace_adapter_layer
2. marketplace_capability_registry
3. marketplace_payload_mapper
4. marketplace_verify_router
5. marketplace_error_playbooks

## Rejected approach
- Do not hardcode all business logic inside eBay scripts.
- Do not duplicate listing builder for every marketplace.
- Do not create Amazon live path before eBay visibility verification is solved.
- Do not add multi-market auto-publish without separate approval per marketplace.

## Recommended order
A. Finish architecture audit
B. Define universal listing model
C. Define marketplace adapter interface
D. Stabilize eBay adapter
E. Add marketplace-neutral Telegram dashboard
F. Add Amazon adapter as future controlled block
FINISH. Review before implementation.
STOP. No live marketplace action from this strategy file.
