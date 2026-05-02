# ECOM_OS_V3_SERVER_TELEGRAM_REAL_URL_HANDOFF_20260502_V1

## Purpose
GitHub-only handoff archive for the next ChatGPT chat. This file summarizes the server/Telegram/eBay-readonly integration work completed after the earlier GitHub preparation continuity file.

## Do not expose secrets
- No token values are stored here.
- No `.env` values are stored here.
- Only presence/status/path information is recorded.

## Required operator format
ION / E1 format only:
1. Краткий анализ
2. Текущий layer
3. Следующий шаг
4. ▶️ Где выполнять
5. CMD / действие одним безопасным блоком
6. Проверка
7. Audit
8. Что дальше

Language: Russian only.
Route: A → B → FINISH → STOP.
No parallel branches. No guessing. Verify before execute.

## Previous GitHub continuity archive
Existing GitHub continuity file:
- `storage/tools/ecom_os_v3/NEW_CHAT_WINDOWS_FULL_LOCAL_CHECK_CONTINUATION_V1.md`

That older file covered GitHub/Windows package preparation and stated next action as Windows local check.
This new archive continues after Windows/server transition and Telegram/eBay-readonly integration.

## Authoritative runtime and repo
GitHub repo:
- `ionlipca7-boop/-ecom-listing-agent-mvp`

Server runtime path:
- `/home/ionlipca7/runtime_eco_v1`

Do not use server as archive/polygon. Server is runtime/production only.
GitHub is canon/design/archive/source layer.

## Current confirmed A → B → FINISH → STOP state

### A — Transfer to server
Status: PASS
- ECOM OS V3 package exists on server.
- Windows → server transfer confirmed by previous states.

### B — Package / agents / adapters
Status: PASS
- Package count from audit: 63 files.
- Python files: 38.
- Agents: 24.
- Adapters: 7 after canonical eBay OAuth/read-only adapters were added.

Agents recorded in master audit:
- `agents/archive_package_agent_v1.py`
- `agents/cleanup_archivist_agent_v1.py`
- `agents/control_orchestrator_agent_v1.py`
- `agents/critic_agent_v1.py`
- `agents/cross_sell_bundle_agent_v1.py`
- `agents/evidence_agent_v1.py`
- `agents/html_agent_v1.py`
- `agents/image_critic_agent_v1.py`
- `agents/inventory_reorder_agent_v1.py`
- `agents/item_specifics_agent_v1.py`
- `agents/listing_health_dashboard_agent_v1.py`
- `agents/listing_lifecycle_agent_v1.py`
- `agents/marketplace_access_gate_agent_v1.py`
- `agents/marketplace_rules_agent_v1.py`
- `agents/photo_blueprint_agent_v1.py`
- `agents/price_competition_agent_v1.py`
- `agents/product_passport_agent_v1.py`
- `agents/promotion_offers_agent_v1.py`
- `agents/security_secrets_guard_agent_v1.py`
- `agents/system_audit_agent_v1.py`
- `agents/teacher_agent_v1.py`
- `agents/title_agent_v1.py`
- `agents/url_intake_agent_v1.py`
- `agents/variation_agent_v1.py`

Key adapters now include:
- `adapters/ebay_oauth_token_guard_v1.py`
- `adapters/ebay_trading_readonly_adapter_v1.py`
- `adapters/marketplace_url_router_v1.py`
- `adapters/ebay_dry_run_payload_builder_v1.py`
- `adapters/telegram_preview_adapter_v1.py`
- `adapters/image_generation_adapter_v1.py`
- `adapters/canva_template_adapter_v1.py`

### C — Telegram preview command
Status: PASS
- Bot running in tmux session `ecom-bot`.
- Existing command `/ecom_os_v3_preview` present.
- Phone preview test confirmed before this handoff.

### D — Telegram draft command
Status: PASS after fix
- Draft bridge created:
  - `storage/tools/ecom_os_v3/server/telegram_ecom_os_v3_draft_route_bridge_v1.py`
- Command added to `bot.py`:
  - `/ecom_os_v3_draft`
- Initial phone test exposed error: `name 'subprocess' is not defined`.
- Fix applied: subprocess import added; bot restarted.
- Phone retest confirmed Telegram returned:
  - `ECOM OS V3 — DRAFT ROUTE PREVIEW`

### E — eBay OAuth token guard
Status: PASS
- Old Trading AuthnAuth path failed with eBay error code 932:
  - `Das Authentifizierungs-Token ist endgültig abgelaufen.`
- Corrected path uses OAuth refresh and `X-EBAY-API-IAF-TOKEN`.
- Canonical guard created:
  - `/home/ionlipca7/runtime_eco_v1/storage/tools/ecom_os_v3/adapters/ebay_oauth_token_guard_v1.py`
- Refresh result:
  - HTTP 200
  - access token received
  - expires_in 7200
  - env file not overwritten
  - no secret printed

### F — eBay canonical readonly adapter
Status: PASS
- Canonical Trading readonly adapter created:
  - `/home/ionlipca7/runtime_eco_v1/storage/tools/ecom_os_v3/adapters/ebay_trading_readonly_adapter_v1.py`
- Result file:
  - `/home/ionlipca7/runtime_eco_v1/storage/state_control/ebay_trading_readonly_adapter_v1_result.json`
- Trading Ack: Success
- Unique active eBay item count: 58
- OAuth guard status: PASS_EBAY_OAUTH_ACCESS_TOKEN_READY
- RequesterCredentials used: false
- X-EBAY-API-IAF-TOKEN used: true
- No live eBay write performed
- No Telegram send performed by that block
- No delete performed
- No secret printed

### G — ECOM OS V3 orchestrator binding
Status: PASS
- Binding state:
  - `/home/ionlipca7/runtime_eco_v1/storage/state_control/ecom_os_v3_canonical_ebay_readonly_orchestrator_binding_v1.json`
- Agent matrix:
  - `/home/ionlipca7/runtime_eco_v1/storage/state_control/ecom_os_v3_agent_activation_matrix_no_live_v1.json`
- Recommended order:
  1. control orchestrator
  2. url intake and product passport
  3. evidence/photo/title/specifics/html/critic/teacher
  4. Telegram preview/draft route
  5. eBay dry-run payload
  6. eBay readonly snapshot
  7. approval gate
  8. live write gate later only

### H — Real product URL route
Status: READY / in progress
Current real product URL from operator:
- `https://www.alibaba.com/product-detail/240w-Charging-Cable-With-Phone-Stand_10000038437444.html?spm=a2756.trade-list-buyer.0.0.63a176e9ltMF49`

Marketplace URL router created:
- `storage/tools/ecom_os_v3/adapters/marketplace_url_router_v1.py`

Router supported marketplaces:
- Alibaba
- AliExpress
- Temu
- eBay
- Amazon

Router tests passed:
- Alibaba product-detail ID: PASS, product_id `10000038437444`
- AliExpress `/item/<id>.html`: PASS
- Temu `goods_id`: PASS
- eBay `/itm/<id>?var=<variant>`: PASS
- Amazon `/dp/<ASIN>`: PASS
- Unknown marketplace: BLOCKED_UNSUPPORTED_MARKETPLACE_URL with Russian operator reply rule

Real URL intake bridge created:
- `storage/tools/ecom_os_v3/server/telegram_ecom_os_v3_real_url_intake_bridge_v1.py`

Real URL intake packet created:
- `storage/state_control/real_product_url_intake_packet_v1.json`

Preview text confirmed in Russian:
- `ECOM OS V3 — ссылка товара принята`
- Platform: Alibaba
- Product ID: `10000038437444`
- Canonical key: `alibaba:10000038437444`

Next action from that state:
- `REVIEW_REAL_URL_INTAKE_BRIDGE_THEN_APPROVE_BOT_AUTO_URL_PATCH_V1`

### I — Telegram Russian control contract
Status: READY, patch not applied
Contract created:
- `storage/tools/ecom_os_v3/server/telegram_control_contract_ru_v1.json`
- `storage/tools/ecom_os_v3/server/telegram_control_contract_ru_v1.md`

Commands in contract:
- `/ecom_help` — показать помощь на русском
- `/ecom_status` — показать состояние проекта
- `/ecom_preview` — alias to preview route
- `/ecom_draft` — alias to draft route
- `/ecom_cancel` — cancel current product route safely, no delete
- `/ecom_files` — show accepted photos/receipts/files for current route

Inline button plan:
- Собрать черновик
- Добавить фото
- Добавить чек
- Показать статус
- Отмена

Patch draft created but NOT applied:
- `storage/state_control/bot_patch_draft_telegram_control_ru_no_apply_v1.txt`

Important inspection after user noticed broken block:
- `bot.py` currently has old preview and draft commands.
- `subprocess_import_present`: true
- new Russian commands are not yet applied
- `plain_url_auto_detect_present`: false
- `bridge_exists` for a separate Telegram control RU bridge was false in inspection

Current next action after inspection:
- `DECIDE_FIX_OR_SAFE_REAPPLY_TELEGRAM_CONTROL_RU_PATCH_V1`

## Current exact blocker / issue
The previous Telegram RU control patch planning stage did NOT apply the new Russian command layer. It only produced a patch draft.
Inspection showed:
- `/ecom_help`: missing
- `/ecom_status`: missing
- `/ecom_preview`: missing
- `/ecom_draft`: missing
- `/ecom_cancel`: missing
- `/ecom_files`: missing
- plain URL auto-detect in bot: missing
- old `/ecom_os_v3_preview`: present
- old `/ecom_os_v3_draft`: present

Therefore the next chat must NOT assume Russian Telegram control is applied.
It must first safely build/apply a corrected bot patch or bridge route, with backup, AST checks, no eBay call, no live write, no delete, no secret print, and restart gate.

## Confirmed mistakes / do not repeat
- Do not treat HTTP 200 or returncode 0 as eBay success; always parse eBay Ack and Errors.
- Do not classify Trading API POST transport as write automatically; GetMyeBaySelling is a read call even though transport is POST.
- Do not use old AuthnAuth `RequesterCredentials/eBayAuthToken` path for current Trading API readonly.
- Use OAuth refresh + `X-EBAY-API-IAF-TOKEN`.
- Do not print token values.
- Do not overwrite `.env` while refreshing OAuth for readonly.
- Do not patch bot.py without backup + AST before/after.
- Do not restart bot without restart gate.
- Do not run server cleanup/delete without separate cleanup gate.
- Do not use server runtime as archive/polygon.
- Do not continue after broken patch state without inspecting actual files and markers.
- Do not write GitHub/server changes blindly without explicit environment and exact path.

## Current operator concern to preserve
Ion asked whether the assistant was creating everything now or correcting existing GitHub files. Correct answer:
- GitHub already had the ECOM OS V3 package and old continuity.
- Server work during this chat was mostly integration/binding/correction around the already transferred package.
- Some missing runtime bridge files/adapters were created on server because integration gaps were found.
- For long-term canon, the new work must be archived/synced to GitHub, not left only on server.

## Product route next goal
Operator provided real Alibaba URL for a product:
- 240W charging cable with phone stand
- Product ID: `10000038437444`

Operator also mentioned a purchase receipt/screenshot with quantity/cost in USD and wants conversion to EUR later.
Important: if receipt/screenshot is provided in Telegram/chat, system must intake it as receipt evidence, not print secrets.

Operator wants Telegram prompts in Russian only, not English fields like Quantity/Target price/Photo requirements/Notes.
Future Russian template should use:
- Ссылка товара
- Количество
- Закупочная цена
- Желаемая цена продажи
- Требования к фото
- Заметки

## Recommended immediate next route in new chat
Start from GitHub archive + current runtime inspection, then continue safely:

1. Read this archive in GitHub.
2. Do NOT use server as archive.
3. Continue at:
   - `DECIDE_FIX_OR_SAFE_REAPPLY_TELEGRAM_CONTROL_RU_PATCH_V1`
4. First safe action:
   - inspect current `bot.py`, existing bridges, and the patch draft;
   - create a single corrected Russian Telegram control bridge if missing;
   - apply bot patch only after backup + AST + marker checks;
   - no eBay API call;
   - no live write;
   - no delete;
   - no secret print;
   - restart only after restart gate.
5. After Telegram RU control works from phone:
   - test plain Alibaba URL message from Telegram;
   - verify Russian preview response;
   - then run real product dry draft route;
   - then handle photos/receipt intake;
   - only then review draft.

## Next allowed action
`DECIDE_FIX_OR_SAFE_REAPPLY_TELEGRAM_CONTROL_RU_PATCH_V1`

## STOP
STOP_AFTER_GITHUB_HANDOFF_ARCHIVE_V1
