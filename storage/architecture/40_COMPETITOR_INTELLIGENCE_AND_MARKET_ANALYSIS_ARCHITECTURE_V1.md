# 40_COMPETITOR_INTELLIGENCE_AND_MARKET_ANALYSIS_ARCHITECTURE_V1

Status: COMPETITOR_INTELLIGENCE_ARCHITECTURE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the competitor intelligence and market analysis architecture for ECOM OS.

This layer helps decide what to buy, how to price, how to position, whether to advertise, and when to avoid weak products.

## External practice alignment
This strategy follows:
- marketplace research based on sold/demand data;
- pricing intelligence;
- search/purchase/review signal analysis;
- niche saturation review;
- seasonal trend analysis;
- safe and compliant data collection boundaries;
- human/operator review for strategic decisions.

## Core decision
Competitor Intelligence recommends.
Brain governs.
Marketplace Adapters execute only after validation and approval.

Correct route:

```text
Market Data Sources
 -> Competitor Intelligence
 -> Product/Price Recommendation
 -> Brain Governance
 -> Operator Review
 -> Marketplace Adapter
```

Forbidden route:

```text
Competitor Intelligence -> direct price change / publish / ad activation
```

## Data sources
Preferred sources:
- official marketplace seller tools;
- sold/completed listing data where available;
- marketplace search signals;
- price history;
- review/feedback patterns;
- category demand signals;
- internal performance history.

Examples:
- eBay Terapeak / Seller Hub research data;
- Amazon Product Opportunity Explorer / Seller Central insights;
- future marketplace analytics tools;
- internal sales and inventory history.

## Market signals
Track:
- average sold price;
- sell-through rate;
- total sold quantity;
- listing count / competition level;
- top listing patterns;
- shipping price/speed;
- return policy patterns;
- review/complaint patterns;
- seasonal trend;
- search volume / keyword demand;
- price trend direction.

## Pricing intelligence
Outputs:
- low market price;
- median market price;
- high market price;
- recommended target price;
- minimum profitable price;
- aggressive price;
- margin risk;
- ad-safe max rate.

Pricing must consider:
- purchase cost;
- shipping cost;
- marketplace fees;
- ad cost;
- return risk;
- stock holding risk.

## Product opportunity scoring
Candidate score should include:
- demand strength;
- competition level;
- margin potential;
- seasonality;
- review pain points;
- bundle opportunity;
- variation opportunity;
- inventory risk;
- marketplace rule risk;
- AI-search readiness.

## Listing improvement recommendations
Competitor Intelligence may recommend:
- better title pattern;
- stronger images;
- bundle strategy;
- variation strategy;
- price adjustment;
- shipping improvement;
- ad/offer strategy;
- category review;
- avoid purchase if demand is weak.

## Safe collection boundaries
Allowed:
- official APIs/tools;
- manual/operator-provided data;
- compliant public data review;
- rate-limited and ToS-aware collection;
- robots-aware collection where applicable.

Forbidden:
- bypassing access controls;
- ignoring legal/ToS risks;
- credential misuse;
- collecting personal data unnecessarily;
- copying competitor content directly;
- scraping that harms services;
- automatic price manipulation without review.

## Anti-manipulation rules
The system must not:
- coordinate prices with competitors;
- generate fake reviews;
- copy competitor copyrighted descriptions;
- manipulate marketplace signals;
- create misleading scarcity;
- generate false demand claims.

## Brain governance boundary
Competitor Intelligence can output:

```json
{
  "recommendation": "",
  "confidence": 0,
  "evidence": [],
  "risk_notes": [],
  "requires_operator_review": true
}
```

Brain decides if recommendation can proceed to draft, validation, or approval.

## Integration with Inventory Core
Market analysis must consider central inventory:
- available quantity;
- cost basis;
- reserved stock;
- bundle component availability;
- slow-moving stock;
- stale inventory risk.

## Integration with AI Listing Layer
Competitor insights can inform:
- SEO title patterns;
- AEO-friendly facts;
- buyer questions;
- compatibility emphasis;
- bundle positioning;
- price/value messaging.

AI must not copy competitor content.

## STOP conditions
STOP if:
- data source is legally unclear;
- scraping violates access boundaries;
- competitor content is copied directly;
- recommendation would create loss below margin guard;
- automatic price/live action would bypass approval;
- market data is too weak for reliable decision.

STOP: This document defines market intelligence architecture only. It does not perform scraping, price changes, ads, publish, or live marketplace actions.
