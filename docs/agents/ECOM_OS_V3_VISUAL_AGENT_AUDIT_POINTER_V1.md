# ECOM_OS_V3_VISUAL_AGENT_AUDIT_POINTER_V1

## Status
READONLY_AUDIT_POINTER_CREATED_V1

## Purpose
Bind the old ECOM CONTROL ROOM canon, the new marketplace visual agent design canon, and the server cleanup discipline into one current decision/pointer document.

This file is a GitHub/design-layer pointer only. It does not execute server actions, eBay actions, EPS uploads, or cleanup/delete operations.

## Current Decision
`STOP_SERVER_PHOTO_EXPERIMENTS_NOW`

Reason:
- V3 technical PASS but visual FAIL.
- V4 technical PASS but visual FAIL.
- V5 asset gallery showed source assets were mostly not marketplace-ready.
- Server runtime accumulated temporary experiment files.
- Problem is architecture and visual evaluation, not the eBay API route.

## Confirmed Good Runtime Memory
The following facts are carried as project memory and must be re-verified before any future live/server action:

- Existing live listing: `318228151138`.
- Protected price: `10.99 EUR`.
- Protected quantity: `40`.
- Inventory API photo update route technically worked in prior server flow.
- Final visual photo result is not accepted as WOW final.
- No new live photo update is allowed until visual-agent sandbox proof and Telegram human preview PASS.

## GitHub Canon Links
Created design/canon docs:

1. `docs/agents/MARKETPLACE_VISUAL_LISTING_AGENT_V1.md`
2. `docs/agents/MARKETPLACE_VISUAL_LISTING_AGENT_V1.schema.json`
3. `docs/agents/SERVER_RUNTIME_CLEANUP_DISCIPLINE_V1.md`

Related older control canon already present in repository:

- `storage/control_layer/project_manifest.json`
- `storage/control_layer/control_rules.json`
- `storage/control_layer/project_state.json`
- `storage/audit/clean_project_boundary_v1.txt`

## Agent Reality Check
`MARKETPLACE_VISUAL_LISTING_AGENT_V1` is currently a design canon and schema, not yet an executable photo generator.

Therefore:
- It has not yet created new product photos.
- It has not yet passed visual sandbox testing.
- It must not be sent to production server yet.
- It must not touch live eBay yet.
- It must not be trusted only because a document says PASS.

## Required Proof Before Server Deployment
Before any server deployment, the visual agent must pass a sandbox proof route:

1. `CREATE_LOCAL_OR_GITHUB_SANDBOX_VISUAL_AGENT_TEST_HARNESS_V1`
2. Input one known product photo set.
3. Build Product Passport.
4. Build Evidence Map.
5. Run Visual Asset Qualification.
6. Build Photo Pack Blueprint.
7. Create or select output image pack in sandbox only.
8. Produce a human-viewable gallery/contact sheet.
9. Run Marketplace Critic.
10. Human operator visually reviews the gallery.
11. Only after visual PASS can server implementation be considered.

## Visual Proof Requirement
Any future claim that the agent works must include visible output, not just JSON.

Minimum required proof package:
- original source gallery
- selected/rejected asset table
- generated/edited final image pack
- numbered contact sheet
- critic report
- clear BLOCK/PASS decision

## Server Cleanup Position
Cleanup is needed later but not now.

Allowed only after:
1. `READONLY_SERVER_RUNTIME_POLLUTION_AUDIT_V1`
2. file classification:
   - KEEP_WORKING_RUNTIME
   - KEEP_FINAL_PROOF
   - ARCHIVE_THEN_DELETE_CANDIDATE
   - DELETE_FORBIDDEN
3. archive zip creation
4. SHA256 verification
5. cleanup manifest
6. explicit operator approval phrase
7. delete candidates only
8. runtime verify after cleanup

No delete from this pointer document.

## Next Allowed Action
`CREATE_LOCAL_OR_GITHUB_SANDBOX_VISUAL_AGENT_TEST_HARNESS_V1`

Scope:
- GitHub/design or local Windows sandbox only.
- No server.
- No EPS.
- No live eBay.
- No cleanup/delete.

## Stop Rule
If the next step cannot produce a visual gallery for human review, stop and do not claim agent readiness.
