# 39_AI_LISTING_AND_AEO_GENERATION_ARCHITECTURE_V1

Status: AI_LISTING_AEO_ARCHITECTURE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the AI listing generation and AEO/AI-search architecture for ECOM OS.

The AI listing layer must generate high-quality candidate content and structured product facts, but it must not publish or mutate marketplace state.

## External practice alignment
This architecture follows:
- structured product data practice;
- marketplace attribute/schema validation;
- semantic search optimization;
- AI-search / answer-engine readiness;
- anti-spam and human-review principles;
- marketplace-safe content generation.

## Core decision
AI Listing Layer generates candidates.
Brain Governance decides whether the candidate may move forward.
Marketplace Adapter translates candidate content into marketplace payload.
Approval Gate controls live action.

Correct route:

```text
Universal Product Model
 -> AI Listing Generator
 -> Quality Score
 -> Marketplace Validation
 -> Approval Gate
 -> Marketplace Adapter
```

Forbidden route:

```text
AI Listing Generator -> Marketplace Publish
```

## AI listing outputs
AI layer may generate:
- German SEO title;
- AEO/AI-search-friendly title variant;
- short subtitle/summary;
- structured product facts;
- German description;
- marketplace-safe HTML candidate;
- compatibility section;
- use cases;
- FAQ/buyer questions;
- bullet points;
- variant/bundle descriptions;
- image text suggestions.

## AI listing inputs
AI layer should consume:
- universal product facts;
- supplier facts;
- normalized attributes;
- variant data;
- bundle data;
- competitor intelligence;
- price/margin constraints;
- marketplace restrictions;
- photo metadata;
- inventory availability.

AI layer must not consume:
- secrets;
- live tokens;
- direct marketplace write credentials;
- uncontrolled raw runtime state.

## SEO + AEO coexistence
SEO content targets marketplace and search engines.
AEO/GEO content targets answer engines and AI-assisted discovery.

Both must be based on true structured facts.

Allowed:
- clear product identity;
- compatibility;
- use cases;
- structured attributes;
- buyer intent language;
- comparison-friendly facts.

Forbidden:
- fake claims;
- keyword stuffing;
- AI slop;
- misleading compatibility;
- unverified certifications;
- invented brand/model support.

## Structured facts schema
Candidate structure:

```json
{
  "product_identity": {},
  "seo_title_de": "",
  "aeo_title_de": "",
  "short_summary_de": "",
  "description_de": "",
  "html_candidate": "",
  "facts": [],
  "compatibility": [],
  "use_cases": [],
  "buyer_questions": [],
  "variants": [],
  "bundle_notes": [],
  "risk_notes": []
}
```

## Marketplace boundaries
AI layer does not decide final marketplace payload validity.

Marketplace Validation Engine must check:
- eBay item specifics/aspects;
- eBay variation support;
- Amazon product type schema;
- required attributes;
- title length;
- image rules;
- category-specific restrictions.

## HTML boundaries
HTML candidate must be:
- marketplace-safe;
- simple;
- mobile-readable;
- no scripts;
- no tracking pixels;
- no unsupported external dependencies;
- no hidden text.

## Human/operator review
AI-generated listing content must pass:
- Quality Score;
- Marketplace Validation;
- Brain Governance;
- Approval Gate.

Operator must receive Russian explanation and German listing preview.

## Anti-garbage rules
Reject candidate if:
- content contradicts product facts;
- title contains spam/keyword stuffing;
- compatibility is invented;
- description is generic filler;
- HTML is unsafe;
- marketplace attributes are missing;
- buyer cannot understand what is included.

## Future AI-search visibility
Future extensions may include:
- structured product JSON-LD export for own shop;
- marketplace-specific attribute enrichment;
- AI-answer optimized FAQs;
- comparison-ready product facts;
- semantic compatibility graph.

## STOP conditions
STOP if:
- AI layer tries to publish;
- AI layer mutates inventory;
- AI layer bypasses validation;
- AI layer bypasses approval;
- AI layer uses secrets;
- AI layer invents unsupported claims.

STOP: This document defines AI listing/AEO architecture only. It does not authorize live generation or publish.
