# MARKETPLACE_VISUAL_LISTING_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Create a controlled marketplace visual listing agent that understands the product, validates evidence, qualifies visual assets, builds compliant photo packs, and blocks live updates until human review passes.

## Root Problem
Previous photo routes failed visually because image choice was based on filenames, dimensions, and technical pass criteria, not real marketplace visual understanding.

## Source Alignment
This design extends the existing ECOM CONTROL ROOM canon:

1. manifest
2. rules
3. state
4. history
5. control_agent
6. archivist_agent
7. runner_agent
8. n8n_orchestration
9. compact_core_migration

This design must not replace the control layer. It adds a visual marketplace agent layer governed by the same A -> B -> FINISH -> STOP discipline.

## Non-Negotiable Rules
- No title, photos, specs, description, or price logic before PRODUCT_PASSPORT_PASS.
- No photo pack before VISUAL_ASSET_QUALIFICATION_PASS.
- Filename-only image selection is forbidden.
- Technical image validation is not enough.
- Main image must be a clean product hero.
- Main image must not contain added text, border, watermark, marketing graphics, fake badge, fake logo overlay, or misleading feature claims.
- If source assets are weak, the system must BLOCK and route to image-edit/generation/remediation, not fake PASS.
- Telegram human preview is mandatory before any live photo update.
- Server is production/runtime only.
- Experiments must happen in GitHub design branch or sandbox, not production server.
- No live eBay/EPS/Inventory update from this design doc.

## Marketplace Rules Baseline

### eBay
- Minimum one image required.
- Minimum 500 px on the longest side.
- Photos must accurately represent the item.
- Added text, artwork, marketing material, borders, and watermarks are forbidden.
- Multiple photos are recommended.

### Amazon-style Quality Baseline
Used as stricter quality inspiration for the main hero image:
- Clean white or neutral background.
- Product dominates frame.
- No overlay text, logos, graphics, borders, watermarks.
- Product must be clearly visible, sharp, and accurate.

## Agent Architecture

### 01_PRODUCT_UNDERSTANDING_AGENT
Purpose:
Understand the real product before any listing or image decision.

Inputs:
- raw product notes
- SKU
- seller-provided images
- product URL if available
- existing listing data if available

Output:
- Product Passport

PASS requires:
- product identity known
- included items known
- variant/color/quantity known
- key visible features known
- uncertainty list empty or acceptable

BLOCK if:
- product identity unclear
- included items unclear
- bundle quantity unclear
- photos contradict product claim

### 02_EVIDENCE_AGENT
Purpose:
Verify every claim against available evidence.

Output:
- Evidence Map

Rules:
- Every visible feature must map to image/source/spec evidence.
- No fake features.
- No invented compatibility.
- No hallucinated specs.

### 03_MARKETPLACE_RULES_AGENT
Purpose:
Load marketplace photo/listing rules before building assets.

Output:
- Rules Checklist

Rules:
- eBay compliance is mandatory.
- Amazon-style hero quality is used as stricter visual standard.
- If eBay and Amazon-style rules conflict, eBay listing rules win for eBay live actions.

### 04_VISUAL_ASSET_QUALIFIER_AGENT
Purpose:
Score each source image visually, not by filename.

Checks:
- product clearly visible
- correct product/bundle
- sufficient resolution
- no foreign text problem
- no watermark
- no heavy compression
- no misleading props
- no duplicate angle unless useful
- suitable for main hero / secondary / detail / reject

Output:
- Asset Qualification Table

PASS requires:
- at least 1 main-hero candidate
- enough secondary candidates for useful gallery
- rejected images explained

BLOCK if:
- no main-hero candidate
- all assets look marketplace-unready
- source pack is visually weak

### 05_PHOTO_DIRECTOR_AGENT
Purpose:
Design final photo pack plan before image tools run.

Output:
- Photo Pack Blueprint

Slots:
1. MAIN_HERO_CLEAN_PRODUCT
2. ANGLE_FRONT_OR_BUNDLE_VIEW
3. DETAIL_CLOSEUP
4. SCALE_OR_USE_CONTEXT
5. INCLUDED_ITEMS_LAYOUT
6. BACK_SIDE_OR_CONNECTOR_DETAIL
7. OPTIONAL_SECONDARY_NO_TEXT
8. OPTIONAL_SECONDARY_NO_TEXT
9. OPTIONAL_SECONDARY_NO_TEXT

Rules:
- MAIN image no text.
- Secondary images no misleading text.
- No fake infographic if evidence is weak.
- German text belongs in title/description, not image, unless marketplace-safe secondary content is explicitly allowed later.

### 06_IMAGE_TOOL_ROUTER_AGENT
Purpose:
Choose safe tool route.

Routes:
- USE_AS_IS when image already compliant.
- CLEAN_BACKGROUND when product is good but background poor.
- CROP_CENTER_SQUARE_1600 when framing is poor.
- REMOVE_FOREIGN_TEXT only if it does not alter product truth.
- GENERATE_REPLACEMENT only if source is unusable and product truth is fully known.
- BLOCK_FOR_HUMAN_PHOTO_REQUEST if truth/evidence is insufficient.

Forbidden:
- fake features
- fake product shape
- fake included items
- fake brand marks
- fake certifications
- watermark/logo overlay
- marketing text on main image

### 07_LISTING_BUILDER_AGENT
Purpose:
Build German eBay listing only after Product Passport and Evidence Map pass.

Outputs:
- SEO title
- item specifics draft
- German description
- price/quantity preservation plan if updating existing listing
- image order plan

Rules:
- Existing live price and quantity must remain unchanged unless operator approves price/quantity scope.
- For listing 318228151138, price 10.99 EUR and quantity 40 are protected.

### 08_MARKETPLACE_CRITIC_AGENT
Purpose:
Critic must evaluate visual quality and policy, not only dimensions.

Checks:
- eBay policy compliance
- main hero quality
- mobile thumbnail clarity
- evidence consistency
- no misleading content
- no text/watermark/border
- no duplicate/low-value images
- final pack looks professional

PASS requires:
- technical PASS
- visual PASS
- policy PASS
- evidence PASS

### 09_TELEGRAM_REVIEW_AGENT
Purpose:
Send human preview before any live update.

Must show:
- final image grid
- protected listing ID/SKU
- price/quantity unchanged notice
- exact intended action
- explicit approve/reject buttons or phrase

No live update without Telegram/operator approval.

### 10_TEACHER_AGENT
Purpose:
Convert every failure into reusable rule.

Stores:
- failure reason
- blocked condition
- new checklist rule
- regression test idea

### 11_CLEANUP_ARCHIVIST_AGENT
Purpose:
Prevent server pollution.

Rules:
- Server temp files are not deleted immediately.
- Cleanup must follow SERVER_RUNTIME_CLEANUP_DISCIPLINE_V1.
- Archive before delete.
- Hash before delete.
- Explicit operator approval before delete.

## Required Gates

### GATE_01_PRODUCT_PASSPORT
PASS before any output.

### GATE_02_EVIDENCE_MAP
PASS before claims/specs/title/photo routing.

### GATE_03_VISUAL_ASSET_QUALIFICATION
PASS before photo pack.

### GATE_04_PHOTO_BLUEPRINT
PASS before image tools.

### GATE_05_MARKETPLACE_CRITIC
PASS before Telegram preview.

### GATE_06_TELEGRAM_REVIEW
PASS before any live update.

### GATE_07_LIVE_UPDATE
Requires explicit operator approval, token guard, readonly before/after verification.

## Stop Conditions
- Missing product identity.
- Bad assets.
- No main hero.
- Unverified feature claim.
- Marketplace rule conflict.
- Server experiment requested.
- Live update requested before Telegram approval.
- Cleanup requested without cleanup gate.

## Protected Existing Listing Rule
For listing 318228151138:
- price 10.99 EUR is protected
- quantity 40 is protected
- no title/category/photo/live mutation without explicit live gate

## Next Allowed Implementation Step
Create schema file:
`docs/agents/MARKETPLACE_VISUAL_LISTING_AGENT_V1.schema.json`
