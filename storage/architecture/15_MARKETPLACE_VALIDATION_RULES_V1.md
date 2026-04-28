# 15_MARKETPLACE_VALIDATION_RULES_V1

Status: DRAFT_RULES_ONLY
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Purpose
Define the validation layer required before any product is converted into a marketplace listing payload.

## Core rule
No marketplace payload may be created or submitted without marketplace-specific validation.

## Validation flow

```text
Universal Product Model
  -> Listing Quality Score
  -> Marketplace Capability Check
  -> Marketplace Rule Validator
  -> Approval Gate
  -> Marketplace Adapter
  -> API Response
  -> Real Visibility Verify
```

## eBay validation requirements
- Check category compatibility.
- Check required item specifics.
- Check title length and marketplace title rules.
- Check image count and image readiness.
- Check variation support for selected category.
- Check variation matrix: SKU, price, quantity, pictures.
- Check business policies: payment, fulfillment, return.
- Check price, quantity, and inventory availability.
- Check promoted listing eligibility before ad recommendation.
- Validate that publish success is followed by real active visibility verification.

## Amazon validation requirements (future)
- Check marketplace and seller account readiness.
- Check product type.
- Load product type schema.
- Validate required attributes.
- Validate variation theme.
- Validate parent-child relationship.
- Validate images against product type rules.
- Validate price and stock.
- Validate fulfillment mode: FBA/FBM.
- Validate listing restrictions before submit.

## Other marketplaces
Every future marketplace must define:
- required fields
- optional fields
- category taxonomy
- image rules
- price rules
- inventory behavior
- variation/bundle support
- advertising support
- verification method

## Validator output schema

```json
{
  "marketplace": "ebay",
  "status": "PASS | FAIL | WARNING",
  "blocking_errors": [],
  "warnings": [],
  "required_fixes": [],
  "can_publish": false,
  "requires_operator_approval": true
}
```

## Blocking conditions
- Missing required category fields.
- Missing required item specifics / attributes.
- Missing stock.
- Missing images.
- Unsupported variation structure.
- Unsupported bundle structure.
- Price below margin guard.
- Unverified marketplace policy.
- No operator approval.

## Non-blocking warnings
- Weak title.
- Low photo count but above minimum.
- Price above market range.
- Description quality below ideal but acceptable.
- Missing AI-search buyer questions.

## Safety
- Validation is read-only.
- Validation must never call publish.
- Validation must never call revise/delete.
- Validation must never touch server secrets.

FINISH: Validation rules defined.
STOP: No runtime action from this file.
