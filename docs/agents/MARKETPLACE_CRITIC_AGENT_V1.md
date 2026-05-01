# MARKETPLACE_CRITIC_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Prevent fake PASS, hallucinated claims, bad images, wrong language, and unsafe live updates.

The critic is mandatory between sandbox generation and Telegram approval.

## Inputs
- Product Passport
- Evidence Map
- source packet
- photo pack
- title options
- item specifics
- HTML description
- marketplace rules
- protected live fields if updating existing listing

## Outputs
- PASS or BLOCKED
- issue list
- required rework action
- exact next_allowed_action

## Required Checks

### Product truth
- product identity known
- bundle quantity known
- visible features match evidence
- unknowns preserved

### Evidence
- all claims backed by source, screenshot, real photo, or operator-provided evidence
- no fake measurements
- no fake compatibility
- no fake certification
- no fake brand

### Language
- operator language: Russian
- eBay Germany content: German only
- no accidental English on German infographic unless approved for EU-wide listing

### Photos
- photo 1: clean main image, no text, no border, no watermark
- photo 2: clean second angle, no text, no border, no watermark
- photos 3-12: infographic/use/detail allowed only if truthful and German for DE listing
- product must remain visually consistent
- no misleading accessories or devices unless used only as generic context

### Title
- German
- clear product type first
- no unsupported brand/model
- no keyword spam
- character length tracked

### Item specifics
- consistent with evidence
- unconfirmed brand marked neutral/not confirmed
- condition explicit
- connector/type fields match product truth

### HTML
- German
- clean structure
- no external scripts
- no unsupported claims
- includes caution/condition note if charging/data speed depends on devices

### Protected fields
If updating existing live listing:
- price protected unless scope approves price change
- quantity protected unless scope approves quantity change
- title/category/photos protected unless exact update scope approves change

## PASS Criteria
- all mandatory checks PASS
- photo pack visible
- German content correct
- no critical issues
- next action is Telegram review, not live update

## BLOCK Criteria
- missing evidence
- unverified claim
- wrong language
- bad main image
- inconsistent product identity
- live action requested before Telegram gate
- cleanup/delete requested without cleanup gate

## Output Format

```json
{
  "status": "PASS_OR_BLOCKED",
  "layer": "MARKETPLACE_CRITIC_AGENT_V1",
  "issues": [],
  "required_rework": [],
  "protected_fields_ok": true,
  "next_allowed_action": "TELEGRAM_REVIEW_AGENT_V1"
}
```

## Stop Rule
If critic cannot verify a claim, the claim must be removed or marked unknown. Do not allow fake PASS.
