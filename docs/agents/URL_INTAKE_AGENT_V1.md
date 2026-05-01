# URL_INTAKE_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Turn a product URL into a reliable source intake packet without hallucination.

## Current Problem
AliExpress and Alibaba short/mobile/share links may fail in automated browsing. The agent must not invent product data when a URL cannot be read.

## Inputs
- Direct product URL
- Short/share URL
- Screenshot fallback
- Real photo fallback
- Operator note in Russian

## Outputs
- source_url
- resolved_url if available
- marketplace/source
- product_title_raw
- source_gallery_references
- visible_specs
- variants
- price/MOQ if visible
- bundle quantity
- uncertainty list
- fallback_needed flag

## Route

### 01_TRY_DIRECT_OPEN
Attempt to open URL.

### 02_TRY_RESOLVE_SHORT_LINK
If short link fails, attempt expanded/resolved URL when possible.

### 03_TRY_PAGE_CONTENT_EXTRACTION
Extract title, images, specs, price, variants.

### 04_SCREENSHOT_FALLBACK
If automated URL read fails, request minimum fallback:
- 1 screenshot of title/main image
- 1 screenshot of gallery/options
- 1 screenshot of specs/description if available

### 05_REAL_PHOTO_FALLBACK
If physical product exists, accept 2-10 real photos.

### 06_INTAKE_PACKET
Create structured packet and pass to PRODUCT_UNDERSTANDING_AGENT.

## Hard Rules
- Do not guess product identity from blocked URL.
- Do not claim URL PASS if only screenshot fallback was used.
- Do not copy supplier text blindly into final listing.
- Preserve uncertainty.
- If marketplace/source page has foreign language, translate to German only after evidence mapping.

## Telegram Requirements
Telegram must accept:
- URL pasted by operator
- screenshot upload
- product photo upload
- Russian voice note saying what to do

## PASS Criteria
- product title or identity found
- at least one image/source evidence available
- source type known
- fallback status clear

## BLOCK Criteria
- URL blocked and no fallback evidence
- product identity unclear
- images unavailable

## Next Handoff
PRODUCT_UNDERSTANDING_AGENT
