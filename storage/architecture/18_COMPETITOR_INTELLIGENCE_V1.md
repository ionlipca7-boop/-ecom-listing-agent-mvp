# 18_COMPETITOR_INTELLIGENCE_V1

Status: DRAFT_STRATEGY_ONLY
Branch: architecture-audit-v1

## Purpose
Define how the system researches competitors, market positioning, title patterns, pricing, and listing quality.

## Core principle
The system should not publish blindly. Every important listing should understand the surrounding market.

## Competitor research goals
- Understand active competitor landscape.
- Identify successful patterns.
- Detect weak competitor opportunities.
- Improve pricing and positioning decisions.
- Improve title and image quality.

## Data points

### Listing quality
- Title structure.
- Title keywords.
- Photo count.
- Hero image quality.
- Variation usage.
- Bundle usage.
- Description structure.

### Marketplace positioning
- Price range.
- Shipping speed.
- Return policy.
- Promoted listing usage.
- Bestseller indicators where available.

### Sales signals
- Sold/completed patterns where marketplace allows.
- Watcher/engagement indicators where available.
- Review/reputation indicators.

## Intelligence outputs

```json
{
  "marketplace": "ebay",
  "competitor_snapshot": [],
  "price_range": {},
  "recommended_positioning": "",
  "title_patterns": [],
  "photo_patterns": [],
  "bundle_opportunities": [],
  "variation_opportunities": [],
  "risk_notes": []
}
```

## Brain recommendations
Examples:
- "конкуренты используют variations, а мы нет"
- "bundle strategy может улучшить margin"
- "на рынке слишком низкая цена"
- "фото конкурентов лучше"
- "title слишком слабый"

## Safety
- Competitor research is advisory.
- Do not copy competitor listings directly.
- Avoid policy violations and duplicate content.
- Recommendations must still pass marketplace validation.

FINISH: Competitor intelligence strategy defined.
STOP: No scraping/runtime action from this file.
