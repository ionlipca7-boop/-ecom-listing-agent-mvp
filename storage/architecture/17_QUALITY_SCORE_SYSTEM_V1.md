# 17_QUALITY_SCORE_SYSTEM_V1

Status: DRAFT_RULES_ONLY
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Purpose
Define the listing quality scoring system before draft approval and before marketplace publish.

## Core rule
No listing should move to publish approval until it has a quality score and blocking issues are resolved.

## Score categories

### 1. Title quality
- German-first title.
- Clear product identity.
- Important keywords included naturally.
- No keyword stuffing.
- Marketplace title length respected.
- Buyer intent included.

### 2. Description quality
- Clean German text.
- Structured sections.
- Benefits and facts separated.
- No garbage text.
- No false claims.
- Mobile-friendly readability.

### 3. HTML/template quality
- Simple marketplace-safe HTML.
- No scripts.
- No unsupported styling.
- Clear headings.
- Good mobile layout.

### 4. Photo quality
- Minimum image count.
- Hero image present.
- Resolution acceptable.
- No bad overlays/watermarks/foreign-language text if avoidable.
- Marketplace photo rules respected.

### 5. Marketplace compliance
- Required item specifics/attributes.
- Category compatibility.
- Variation/bundle support.
- Business policy readiness.
- Price and stock available.

### 6. Price and margin
- Purchase cost known.
- Fees estimated.
- Shipping cost considered.
- Minimum margin protected.
- Competitor price range checked.

### 7. AI-search/AEO/GEO readiness
- Structured facts.
- Compatibility facts.
- Use cases.
- Buyer questions.
- Clear answer-like product explanation.

## Output schema

```json
{
  "quality_score_total": 0,
  "scores": {
    "title": 0,
    "description": 0,
    "html": 0,
    "photos": 0,
    "marketplace_compliance": 0,
    "price_margin": 0,
    "ai_search": 0
  },
  "blocking_errors": [],
  "warnings": [],
  "recommendations": [],
  "can_request_publish_approval": false
}
```

## Suggested gates
- 0-59: fail, must fix.
- 60-74: draft only, not publish-ready.
- 75-89: publish approval allowed with warnings.
- 90-100: strong listing.

## Telegram output in Russian
Example:
"Листинг готов на 82/100. Можно публиковать после твоего подтверждения, но я рекомендую улучшить фото и добавить совместимость."

FINISH: Quality score rules defined.
STOP: No runtime scoring from this file.
