# ECOM OS V3 — SINGLE FLOW CANON ARCHIVE

STATUS: CANON_SINGLE_FLOW_ARCHIVE_CREATED_IN_GITHUB
DATE: 2026-05-03
OPERATOR: Ion
PROJECT: ECOM LISTING AGENT MVP / CONTROL ROOM / ECOM OS V3
LANGUAGE: Russian for operator/project work; German for customer-facing eBay listings.
FORMAT: strict ION / E1.

## Purpose
This file is the canonical single-flow transition archive for the next chat. The next chat must use this archive as the first navigation point in GitHub before creating new steps. It must not restart from scattered server runtime files, Windows local files, old branches, or speculative memory.

Canonical GitHub path:
`storage/memory/archive/ECOM_OS_V3_SINGLE_FLOW_CANON_20260503T1325Z/`

## Verified existing GitHub archive evidence
The current GitHub repository is:
`ionlipca7-boop/-ecom-listing-agent-mvp`

Verified existing GitHub archive package:
`storage/memory/archive/ECOM_OS_V3_LOCAL_AUDIT_AND_BLUEPRINT_ARCHIVE_20260503T105053Z/ARCHIVE_MANIFEST.json`

This existing manifest states:
- status: `PASS_FIX_ARCHIVE_MANIFEST_FULL_SHA256_V2`
- github_target_path: `storage/memory/archive/ECOM_OS_V3_LOCAL_AUDIT_AND_BLUEPRINT_ARCHIVE_20260503T105053Z/`
- source files include local deep project audit, canonical blueprint inputs, canonical blueprint V2 safe JSON/MD, and new chat front.
- current blocker at that archive time: `G3 policy read-only blocked by user token refresh HTTP 400`
- live_gate: `CLOSED`
- next_after_archive: `REVIEW_ARCHIVE_PACKAGE_THEN_OPTIONAL_GIT_COMMIT_GATE_V1`

Verified recent archive commits found in GitHub:
- `2968891` — Archive ECOM OS V3 transition after G2 item specifics and G3 token 400
- `b16ef15` — Archive ECOM OS V3 new product transition V3
- `664e213` — docs: archive ecom os v3 server telegram real url handoff
- `e5cc6ab` — archive: add ECOM OS V3 local audit and blueprint package

## Core correction from this chat
The project must have one current route and one current canon path.

Correct environment roles:
- GitHub: canon/archive/source/experiments/single-flow archive. New chats must read GitHub archive first.
- Server: runtime only. Telegram bot, eBay runtime, token guard, current pointer, live state. Do not use server as archive playground.
- Windows: copy/review workstation only. Not canonical source. Use for local checks or full project copy if needed.
- Telegram: operator cockpit.

Strict rules:
- No parallel branches.
- No live eBay/Amazon write without explicit live gate and operator approval.
- No delete/cleanup without explicit cleanup gate.
- No git pull/merge on dirty server runtime.
- No bot restart without restart gate.
- No token print or secret print.
- If a command fails or logic looks wrong: STOP_SAFE -> inspect -> use GitHub archive / official docs / internet if needed -> then continue.
- User words are operator input, not blind commands. Analyze first. If deviating from user wording, explain briefly and follow the safe route.

## Full project skeleton V3 to FINISH_STOP
A. Archive and register unified skeleton V3 in GitHub.
B. Build server clean runtime construction plan.
C. Implement/control runtime core and registry.
D. Telegram cockpit: text, URL, photo/file, voice dry route.
E. Finanzamt/accounting dry layer.
F. Full product dry route to approval card.
G. One approved live gate only.
H. Post-live readonly verify and archive lesson.
I. Cleanup gate only after stable PASS.
FINISH_STOP: GitHub canon complete, server runtime stable, Telegram cockpit working, marketplace route gated and verified, strategy/accounting reports present.

## What existed before this chat
The project already had:
- ECOM LISTING AGENT MVP control room with manifest/rules/state/history/control_agent/archivist_agent/runner_agent/n8n/compact core principle.
- GitHub bridge and server runtime.
- Telegram bot runtime.
- eBay Trading API readonly verification history.
- eBay token repair and refresh history.
- Live listing UD24 success history.
- Photo agent / listing update route history.
- Windows local deep audit and canonical blueprint V2 archive.

## What was done in this chat, compressed single flow
1. GitHub local audit archive commit/push was verified:
   - Branch: `create-offer-draft-v1`
   - Commit pushed: `e5cc6ab archive: add ECOM OS V3 local audit and blueprint package`
   - Remote verified via `git ls-remote`.
2. Server audit was performed:
   - Root: `/home/ionlipca7/runtime_eco_v1`
   - Branch: `create-offer-draft-v1`
   - Server head at audit time: `3bb6dd0 Add ECOM OS V3 Telegram real product dry review route`
   - Server dirty tree expected.
   - Bot process running.
   - Key paths exist: `bot.py`, `CURRENT_POINTER`, `BLOCK_LEDGER`, `CURRENT_ROUTE_LOCK`, `DEBT_REGISTER`, token policy, project regulation, Telegram contract, G3 runner, token guard.
3. Unified skeleton draft was built from GitHub + Windows + server.
4. Final unified audit conclusion + to-finish skeleton V3 was created.
5. The operator clarified canonical roles:
   - GitHub is the main archive/canon/polygon.
   - Server must stay clean runtime only.
   - Windows is only workstation/copy/review, not canon.
6. Server clean runtime construction plan was created.
7. B1-B6 server runtime plan passed:
   - B1 runtime pointer + route lock review.
   - B2 clean source registry.
   - B3 Telegram cockpit dry contract.
   - B4 voice layer dry design.
   - B5 Finanzamt/accounting dry design.
   - B6 full dry route test plan.
8. B7-B10 approval card route built:
   - B7 dry approval packet schema.
   - B8 dry approval packet example.
   - B9 Telegram approval card renderer dry.
   - B10 bot patch plan.
9. B11-B17 initial `/ecom_dry_card` route:
   - B11 inspected bot anchors.
   - B12 built patch draft.
   - B13 reviewed apply gate.
   - B14 applied bot patch.
   - B15 verified render without restart.
   - B16 restarted bot.
   - B17 Telegram test produced card.
10. Defect found by operator:
   - After `/ecom_dry_card`, bot also replied: `Текст сохранён. Если это ссылка товара — я подготовлю обработку для листинга.`
   - Card was not fully Russian; it had English labels.
   - Card was eBay-centric instead of universal marketplace.
11. B18-B21 repair sequence:
   - B18 registered dry card PASS with fallthrough defect.
   - B19 built fallthrough fix draft.
   - B20 incorrectly applied draft text as code.
   - B21A detected broken block: py_compile failed; draft text inserted.
   - B21B attempted restore from wrong backup and failed because backup was from before dry-card block.
   - B21C correctly reinserted clean dry card block with continue guards; compile PASS.
   - B21D restarted bot.
12. B22/B23 issue:
   - Operator tested again and still got extra text-save message.
   - Assistant incorrectly treated route as pass and then opened live gate dry for eBay/Amazon.
   - Operator corrected: live gate was premature; universal/ru/fallthrough defects must be handled first.
13. B22C draft was created for universal dry card but was not enough:
   - It created a draft path only.
   - It did not yet apply full Russian renderer.
   - It did not fully fix generic text fallthrough.
   - It did not complete multi-marketplace command intelligence.
14. Important operator correction:
   - New chat must not waste time rediscovering this.
   - Archive must be in GitHub, one flow, one location.
   - New chat must read this canon before touching server.

## Current known defects to continue from
DO NOT close route until these are fixed and tested:
1. `/ecom_dry_card` still falls through to generic text-intake and sends extra message:
   `Текст сохранён. Если это ссылка товара — я подготовлю обработку для листинга.`
2. Dry card text is not fully Russian operator cockpit.
3. Dry card is still eBay-centric; it must be universal marketplace card for eBay, Amazon and future German marketplaces.
4. The bot must understand operator natural language in Telegram:
   - `проверь eBay листинги`
   - `проверь Amazon листинги`
   - `дай отчет, какие хорошие, какие плохие`
   - voice input later: voice -> transcript -> intent -> confirmation card -> dry action only.
5. Live gate was opened too early as dry-gate test. Treat it as a route error and do not do live write.
6. Before further bot patch: inspect real `bot.py` command flow and generic text handler; do not guess.

## Correct next route for next chat
NEXT_ALLOWED_ACTION:
`B22A_INSPECT_REAL_BOT_FLOW_FOR_FALLTHROUGH_AND_BUILD_RU_UNIVERSAL_MARKETPLACE_CARD_PLAN_NO_PATCH_V1`

The next chat must:
1. Read this archive file first.
2. Search/fetch prior GitHub archive manifests if needed.
3. Not use server as archive.
4. Not push random server runtime noise.
5. Inspect actual bot.py control flow before patch.
6. Build a patch draft only for:
   - Russian operator card renderer.
   - Universal marketplace fields.
   - handled-command guard to stop `/ecom_dry_card` from reaching generic save_text.
   - command/intent plan for `проверь eBay`, `проверь Amazon`, good/bad report.
7. Apply only after review gate.
8. Restart only after compile PASS.
9. Telegram test must pass with exactly one Russian universal card and no second text-save message.

## Canonical archive behavior for future chats
Every transition to a new chat must create/update a GitHub single-flow archive:
- The archive lives under `storage/memory/archive/` in GitHub.
- It must include a readable README/manifest, not only a zip.
- It must include: current state, what was done, errors, fixes, current blockers, next allowed action, environment roles, and exact continuation prompt.
- New chat prompt must say: "first read GitHub single-flow archive; do not start from server or Windows."

## New chat prompt
ION / E1 NEW CHAT CONTINUATION — ECOM OS V3 SINGLE FLOW

You are continuing the ECOM LISTING AGENT MVP / CONTROL ROOM project for operator Ion.
Language: Russian.
Format: strict ION / E1:
1. Краткий анализ
2. Текущий layer
3. Следующий шаг
4. ▶️ Где выполнять
5. CMD / действие одним безопасным блоком
6. Проверка
7. Audit
8. Что дальше

Start by reading this GitHub canonical archive:
`storage/memory/archive/ECOM_OS_V3_SINGLE_FLOW_CANON_20260503T1325Z/README_FULL_PROJECT_SINGLE_FLOW.md`

Also verify existing older archive manifest:
`storage/memory/archive/ECOM_OS_V3_LOCAL_AUDIT_AND_BLUEPRINT_ARCHIVE_20260503T105053Z/ARCHIVE_MANIFEST.json`

Do not start from server runtime files unless the next step explicitly requires server inspection.
Do not use Windows as canon.
GitHub is the single archive/canon layer.
Server is runtime only.
Windows is local copy/review only.

Current next allowed action:
`B22A_INSPECT_REAL_BOT_FLOW_FOR_FALLTHROUGH_AND_BUILD_RU_UNIVERSAL_MARKETPLACE_CARD_PLAN_NO_PATCH_V1`

Main defects to fix:
- `/ecom_dry_card` still triggers extra generic text-save message after the card.
- Card is not fully Russian.
- Card is eBay-centric and must become universal marketplace cockpit for eBay + Amazon + future marketplaces.
- Bot must understand natural language operator commands for checking eBay/Amazon listings and reporting good/bad listings.

Safety:
- No live eBay/Amazon write.
- No cleanup/delete.
- No git pull/merge on dirty server.
- No bot restart unless compile PASS and restart gate.
- No secret print.
- If one step fails, STOP_SAFE and inspect before next command.

Correct next action:
Build no-patch inspection/report first: find actual `bot.py` fallthrough path and renderer language source; then build patch draft only.
