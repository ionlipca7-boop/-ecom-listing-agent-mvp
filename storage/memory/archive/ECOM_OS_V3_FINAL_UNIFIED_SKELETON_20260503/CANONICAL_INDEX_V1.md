# ECOM OS V3 FINAL UNIFIED SKELETON — CANONICAL INDEX V1

Date: 2026-05-03
Status: CANONICAL_INDEX_ARCHIVED_TO_GITHUB

## Fixed environment roles
- GitHub = canon / archive / source / experiments / project memory.
- Server = clean runtime only: Telegram bot, eBay executors, token guard, runtime state.
- Windows = full project copy / backup / transfer only, not canon.
- Telegram = operator cockpit for inputs, approvals, status, errors, future voice commands.

## Main audit conclusion
We already found working blocks across GitHub, Windows audit, and Server audit. The project problem is not lack of components, but mixed environments, repeated branches, dirty runtime, long broken terminal commands, and missing STOP_SAFE discipline after failures.

## Current working blocks
- Control core: CURRENT_POINTER, BLOCK_LEDGER, CURRENT_ROUTE_LOCK, DEBT_REGISTER, LIVE_GATE, NEXT_ALLOWED_ACTION.
- Telegram runtime: bot.py running, product intake, dry review, approval cards, image/file intake.
- eBay runtime: Trading API readonly, token guard, gated publish/revise, post-live readonly verify.
- Product pipeline: evidence, photo pack, German draft, category/aspects/policy gates, approval, live gate.
- Strategy layer: performance, daily strategy, price optimizer, lifecycle, inventory reorder.

## Missing blocks
- Telegram voice command layer: voice -> transcript -> intent -> confirmation card -> approved action only.
- Finanzamt/accounting layer: sales ledger, purchase evidence, VAT/tax mode registry, monthly report, Steuerberater export packet.
- Marketplace router: eBay first, later Amazon DE / Kleinanzeigen / other German marketplaces via separate adapters.
- Observability: runtime health, token expiry, last readonly verify, last Telegram command, error debt register.
- Server cleanup plan: audit first, protect live state, cleanup only after explicit gate.

## Current blockers
- G3 policy read-only blocker: token/policy issue; no G4/G5/G6 until G3 PASS.
- Server dirty tree: no pull, merge, restart, or cleanup until reviewed.
- Voice layer missing.
- Accounting layer missing.
- Final clean server runtime not yet constructed.

## Route to FINISH_STOP
A. Archive canonical skeleton in GitHub.
B. Build server master registry from existing server audit; no pull/restart/cleanup.
C. Resolve G3 policy blocker with token context policy; no blind OAuth retry.
D. Add Telegram voice dry route.
E. Add accounting/Finanzamt dry report route.
F. Run full dry product route to approval card.
G. Open one approved live eBay gate only.
H. Post-live readonly verify and archive lesson.
I. Run cleanup audit gate only after stable PASS.
FINISH_STOP: GitHub canon complete, server clean runtime stable, Telegram cockpit works, eBay route gated/verified, strategy/accounting reports present.

NEXT_ALLOWED_ACTION=BUILD_SERVER_MASTER_REGISTRY_FROM_EXISTING_AUDIT_NO_PULL_NO_RESTART_NO_CLEANUP_V1
