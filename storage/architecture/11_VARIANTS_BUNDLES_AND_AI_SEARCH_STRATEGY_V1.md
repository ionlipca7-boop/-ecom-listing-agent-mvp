# 11_VARIANTS_BUNDLES_AND_AI_SEARCH_STRATEGY_V1

Status: DRAFT_STRATEGY_ONLY
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Purpose
Add support strategy for multi-quantity listings, marketplace variations, bundles/kits, and AI-search-ready product content.

## Confirmed marketplace capabilities

### eBay
- eBay supports multi-quantity fixed-price listings.
- eBay supports listings with variations such as color, size, material, length, style.
- eBay variation listings can have variation-level quantity, price, SKU, and pictures.
- eBay category support must be checked before variation listing creation.
- eBay Promoted Listings rules may apply advertising at group/listing level for multi-SKU listings.

### Amazon
- Amazon supports parent-child variation relationships.
- Amazon requires a variation theme depending on product type.
- Amazon Product Type Definitions API defines required attributes and schemas per marketplace/product type.
- Variation validation must happen before listing submission.

## Required new blocks

### variant_bundle_engine_block
Role:
- Decide whether a product should be listed as single item, multi-quantity, variation, or bundle.
- Create internal variant matrix.
- Map variants to marketplace-specific payloads.

Supported structures:
1. Single product
2. Multi-quantity same product
3. Variations by color/size/length/material/style
4. Pack quantity variants, e.g. 1 cable / 2 cables / 5 cables
5. Bundle/kits, e.g. cable + adapter, charger + cable
6. Marketplace-specific parent-child or group listing

### bundle_inventory_guard_block
Role:
- Prevent overselling when one bundle consumes multiple stock components.
- Example: Bundle A = 2 cables + 1 adapter.
- When bundle sells, decrement component inventory.

### ai_search_optimization_block
Role:
- Create content useful for traditional marketplace search and AI-assisted discovery.
- Support SEO + AEO/GEO style signals.
- Produce clear structured product facts, use cases, compatibility, comparison phrases, and buyer-intent language.

## Universal product model additions

```json
{
  "product_family_id": "...",
  "listing_mode": "single | multi_quantity | variation | bundle | kit",
  "variants": [
    {
      "variant_sku": "...",
      "attributes": {
        "color": "black",
        "length": "1m",
        "pack_quantity": 2
      },
      "quantity_available": 10,
      "price": {},
      "images": []
    }
  ],
  "bundle_components": [
    {
      "component_sku": "...",
      "quantity_per_bundle": 2
    }
  ],
  "search_content": {
    "traditional_seo": {},
    "ai_search_aeo_geo": {},
    "buyer_questions": [],
    "compatibility_facts": [],
    "use_cases": []
  }
}
```

## Brain decision logic

The Brain should ask:
1. Are there multiple identical units? -> multi_quantity.
2. Are there meaningful options such as color/size/length? -> variation listing.
3. Are there pack sizes? -> pack_quantity variants.
4. Can items be sold together as a better value kit? -> bundle/kit.
5. Does marketplace support this mode in the selected category? -> validator.
6. Is stock safe across all channels and bundle components? -> inventory guard.
7. Is the listing optimized for both marketplace search and AI search? -> content gate.

## eBay rules to respect
- Use fixed-price listing model for multi-quantity and variations.
- Check category variation support before creation.
- Variation-level SKU, price, quantity, and images must be controlled.
- Do not assume an existing non-variation listing can be simply converted into a variation listing.
- Advertising strategy must know whether ad rate applies to whole group/listing.

## Amazon rules to respect
- Use parent-child relationship for variations.
- Select correct product type and variation theme.
- Validate required attributes via Product Type Definitions.
- Do not copy eBay variation structure blindly into Amazon.

## AI search / AEO / GEO strategy

Goal:
Make listing content understandable by humans, marketplace search, Google-like search, and AI assistants.

Content should include:
- exact product identity
- compatibility
- use cases
- buyer questions and answers
- important attributes
- comparison-friendly wording
- structured facts
- clear German language first
- marketplace-specific fields

Do not create fake claims. AI-search optimization must improve clarity, not invent features.

## Implementation priority
P0:
- Add variant/bundle concepts to universal listing model.
- Add marketplace validator requirements for variations.
- Add inventory guard for bundles.

P1:
- Build Brain recommendation: single vs variation vs bundle.
- Add Telegram review screen for variant matrix.

P2:
- Add AI-search content generator.
- Add buyer-question block to listing quality score.

P3:
- Add performance feedback: which variants sell best, which bundles work, which AI/search phrases convert.

## Rejected
- No direct marketplace publish for variations without category/schema validation.
- No bundle listing without component inventory guard.
- No AI-search spam or fake keyword stuffing.
- No copying one marketplace ruleset to another.

FINISH: Strategy recorded for future implementation.
STOP: No live action from this file.
