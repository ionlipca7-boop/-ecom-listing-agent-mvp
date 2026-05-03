# ECOM OS V3 — Server Reality Canon Rebuild — 2026-05-03 15:12Z

## Status

`PASS_SERVER_REALITY_AUDIT_COLLECTED_FOR_CANON_REBUILD`

This archive corrects the previous GitHub handoff confusion. The previous GitHub master index and corrected manifest existed, but they did not reflect the full current server reality for B1-B23 dry card work.

## Verified repositories

- `ionlipca7-boop/-ecom-listing-agent-mvp` — active archive/source repo
- `ionlipca7-boop/ECOM_OS_V3` — checked
- `ionlipca7-boop/ECOM_GOVERNED_RUNTIME` — checked

## Server runtime checked

- Runtime path: `/home/ionlipca7/runtime_eco_v1`
- Server branch: `create-offer-draft-v1`
- Server HEAD: `3bb6dd0`
- Bot process: running as `python3 bot.py`
- tmux session: `ecom-bot`
- Server git status: dirty / runtime contains many untracked and modified files

## Important correction

GitHub archive files are not mirrored on the server:

- `storage/memory/archive/ECOM_OS_V3_CANON_ARCHIVE_INDEX_MASTER/MASTER_ARCHIVE_INDEX.json` missing on server
- `storage/memory/archive/ECOM_OS_V3_SINGLE_FLOW_CANON_CORRECTED_20260503T0930Z/MANIFEST_SINGLE_FLOW.json` missing on server
- `README_FULL_PROJECT_SINGLE_FLOW.md` missing on server and not found on GitHub main

Therefore GitHub remains archive/source-of-truth; server remains runtime only.

## Bot reality

`bot.py`:

- exists: yes
- AST parse: OK
- contains `/ecom_dry_card`: yes
- contains fallthrough markers: yes
- contains Russian text markers: yes
- contains eBay marker: yes
- contains Amazon marker: yes
- handler line: `406`

## Confirmed server B-route from state_control

B1 through B16 are present and PASS. B18 through B23 are present and PASS/recorded. Important entries:

- B1: `PASS_B1_RUNTIME_POINTER_AND_ROUTE_LOCK_REVIEW_NO_LIVE_V1`
- B2: `PASS_B2_BUILD_RUNTIME_CLEAN_SOURCE_REGISTRY_NO_LIVE_V1`
- B3: `PASS_B3_TELEGRAM_COCKPIT_DRY_CONTRACT_NO_PATCH_NO_RESTART_V1`
- B4: `PASS_B4_VOICE_LAYER_DRY_DESIGN_NO_PATCH_NO_RESTART_V1`
- B5: `PASS_B5_FINANZAMT_ACCOUNTING_DRY_DESIGN_NO_PATCH_NO_RESTART_V1`
- B6: `PASS_B6_FULL_DRY_ROUTE_TEST_PLAN_NO_LIVE_NO_PATCH_V1`
- B7: `PASS_B7_BUILD_DRY_APPROVAL_PACKET_SCHEMA_NO_LIVE_NO_PATCH_V1`
- B8: `PASS_B8_BUILD_DRY_APPROVAL_PACKET_EXAMPLE_NO_LIVE_NO_PATCH_V1`
- B9: `PASS_B9_BUILD_TELEGRAM_APPROVAL_CARD_RENDER_DRY_NO_PATCH_V1`
- B10: `PASS_B10_BUILD_BOT_PATCH_PLAN_FOR_DRY_APPROVAL_CARD_NO_APPLY_V1`
- B11: `PASS_B11_INSPECT_BOT_STRUCTURE_FOR_DRY_CARD_PATCH_ANCHOR_NO_APPLY_V1`
- B12: `PASS_B12_BUILD_BOT_PATCH_DRAFT_FOR_DRY_CARD_NO_APPLY_V1`
- B13: `PASS_B13_REVIEW_BOT_PATCH_DRAFT_THEN_APPLY_GATE_V1`
- B14: `PASS_B14_APPLY_BOT_PATCH_DRY_CARD_AFTER_REVIEW_GATE_V1`
- B15: `PASS_B15_VERIFY_DRY_CARD_COMMAND_PATCH_NO_RESTART_V1`
- B16: `PASS_B16_RESTART_BOT_AFTER_DRY_CARD_PATCH_V1`
- B18: `PASS_B18_REGISTER_DRY_CARD_PASS_AND_FIX_FALLTHROUGH_PLAN_NO_APPLY_V1`
- B19: `PASS_B19_BUILD_FALLTHROUGH_FIX_PATCH_DRAFT_NO_APPLY_V1`
- B20: `PASS_B20_APPLY_FALLTHROUGH_FIX_PATCH_V1`
- B21A: `BLOCKED_B21A_BOT_BLOCK_NEEDS_REPAIR`
- B21C: `PASS_B21C_REINSERT_CLEAN_DRY_CARD_BLOCK_WITH_FALLTHROUGH_FIX_V1`
- B22C: `PASS_B22C_BUILD_UNIVERSAL_DRY_CARD_PATCH_DRAFT_NO_APPLY_V1`
- B23: `PASS_B23_OPEN_LIVE_GATE_EBAY_AMAZON_FOR_DRY_CARD_V1`

## Confirmed G-route from state_control

The G marketplace route also exists:

- G1 category selected: PASS
- G2 item specifics: PASS
- G3 policy binding gate: PASS/opened
- G3 token/account permission flow remains blocked:
  - 401 invalid/expired token recorded
  - token refresh failure recorded
  - 403 scope/account permission needs fresh consent plan recorded
  - fresh consent URL generated
  - auth code save preflight blocked

## Route conflict

The server now has a route conflict:

- Latest dry card route says: `B23 -> B24_OPERATOR_TEST_LIVE_GATE_DRY_CARD_V1`
- `CURRENT_ROUTE_LOCK` still says: `G_LIVE_MARKETPLACE_GATE_BLOCK / G3_POLICY_BINDING_READONLY`
- `CURRENT_POINTER` points to older dynamic photo/receipt intake step.

This means the next action is **not** live and not G4/G5/G6. The next action is route reconciliation.

## Correct next_allowed_action

`RECONCILE_CURRENT_POINTER_ROUTE_LOCK_AND_B23_B24_DRY_CARD_GATE_NO_LIVE_V1`

Purpose: define one current route from actual server state:

1. B24 Telegram dry card test route
2. or return to G3 token consent repair route

No live actions until this is reconciled.

## Constraints

- `LIVE_GATE=CLOSED_UNTIL_RECONCILED`
- `NO_LIVE_EBAY_WRITE=YES`
- `NO_LIVE_AMAZON_WRITE=YES`
- `NO_DELETE=YES`
- `NO_PUSH=YES`
- `NO_SECRET_PRINT=YES`
- `NO_BOT_RESTART=YES`
- `WIP_LIMIT=1`

## Final

`CANON_ARCHIVE_REBUILT_FROM_GITHUB_AND_SERVER_REALITY_ON_BRANCH`
