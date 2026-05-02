# NEW_CHAT_WINDOWS_FULL_LOCAL_CHECK_CONTINUATION_V1

## Project
ECOM LISTING AGENT MVP / ECOM OS V3 / CONTROL ROOM

## Operator
Ion / ION

## Language
Russian only.

## Required answer format
Strict ION format:
1. Краткий анализ
2. Текущий layer
3. Следующий шаг
4. ▶️ Где выполнять
5. CMD / действие одним безопасным блоком
6. Проверка
7. Audit
8. Что дальше

## Core rules
- Route: A → B → FINISH → STOP.
- One route only, no parallel branches.
- Verify before execute.
- No live eBay before explicit live gate.
- No delete/cleanup without cleanup gate.
- No blind server overwrite.
- No secrets printed or committed.
- Windows first, server later.
- Server is production/runtime only.
- GitHub is source/design/package layer.

## Current confirmed status
GitHub preparation stage for ECOM OS V3 is complete enough for first Windows local check.

Final GitHub marker:
- `storage/tools/ecom_os_v3/FINISH_GITHUB_PREPARATION_STOP_V1.json`

Current next allowed action:
- `RUN_WINDOWS_FULL_LOCAL_CHECK_V1`

Main Windows entrypoint:
- `storage/tools/ecom_os_v3/run_full_local_check_v1.bat`

Latest package index:
- `storage/tools/ecom_os_v3/PACKAGE_INDEX_V4.json`

Windows next plan:
- `storage/tools/ecom_os_v3/NEXT_WINDOWS_STAGE_PLAN_V1.md`

## What was completed in this chat

### 1. Listing creation core
Created real Python agents under `storage/tools/ecom_os_v3/agents/`:
- `url_intake_agent_v1.py`
- `product_passport_agent_v1.py`
- `evidence_agent_v1.py`
- `marketplace_rules_agent_v1.py`
- `photo_blueprint_agent_v1.py`
- `image_critic_agent_v1.py`
- `title_agent_v1.py`
- `item_specifics_agent_v1.py`
- `html_agent_v1.py`
- `critic_agent_v1.py`
- `teacher_agent_v1.py`
- `system_audit_agent_v1.py`

Purpose:
- create source packet;
- create Product Passport;
- map evidence;
- create photo blueprint;
- critic for visual/photo structure;
- German title;
- German item specifics;
- German HTML preview;
- final critic;
- lessons/teacher output.

### 2. Control brain and safety gates
Created:
- `agents/control_orchestrator_agent_v1.py`
- `agents/security_secrets_guard_agent_v1.py`
- `agents/marketplace_access_gate_agent_v1.py`
- `adapters/ebay_token_preflight_guard_v1.py`

Purpose:
- one brain route control;
- scan for secret-like values;
- block marketplace live route unless access/token/scope/approval gates pass;
- eBay token preflight/refresh only, no listing changes.

### 3. Local runners and checks
Created/updated:
- `local_sandbox_runner_v1.py`
- `e2e_virtual_pipeline_v1.py`
- `portfolio_strategy_runner_v1.py`
- `package_audit_v1.py`
- `bootstrap_verify_local_package_v1.py`
- `run_full_local_check_v1.bat`

Current V4 Windows order:
1. Control Orchestrator
2. Security Secrets Guard
3. Package Audit
4. Bootstrap Verify
5. E2E Listing Pipeline
6. Portfolio Strategy Pipeline
7. STOP

### 4. Test inputs
Created:
- `test_inputs/usb_c_cable_stand_v1.json`
- `test_inputs/usb_adapter_6pcs_v1.json`
- `test_inputs/sample_portfolio_v1.json`

### 5. Post-listing / portfolio strategy
Created real agents:
- `listing_lifecycle_agent_v1.py`
- `promotion_offers_agent_v1.py`
- `cross_sell_bundle_agent_v1.py`
- `listing_health_dashboard_agent_v1.py`
- `variation_agent_v1.py`
- `inventory_reorder_agent_v1.py`
- `price_competition_agent_v1.py`

Purpose:
- 3/5/7/14 day listing health logic;
- promotion/offers logic;
- watched-no-sale / offer candidate;
- cross-sell/bundle suggestions;
- variation safety;
- inventory reorder/hold/do-not-reorder decisions;
- price/competition review using provided snapshots only.

### 6. Archive / cleanup / merge / server transition
Created:
- `agents/archive_package_agent_v1.py`
- `agents/cleanup_archivist_agent_v1.py`
- `state_handoff_schema_v1.json`
- `server/server_readonly_cleanup_audit_v1.py`
- `server/server_existing_runtime_audit_and_diff_v1.py`
- `MERGE_MANIFEST_TEMPLATE_V1.json`
- `deploy_filter_v1.py`

Purpose:
- archive outputs with ZIP + SHA256 + manifest;
- cleanup candidates only after audit/gate;
- state handoff between Windows/server/Telegram/n8n/eBay gates;
- readonly server diff;
- clean deploy filter;
- no blind copy to server.

### 7. Adapter stubs / future integrations
Created safe local adapters:
- `adapters/image_generation_adapter_v1.py`
- `adapters/canva_template_adapter_v1.py`
- `adapters/telegram_preview_adapter_v1.py`
- `adapters/ebay_dry_run_payload_builder_v1.py`

Current status:
- image generation provider not connected;
- Canva not connected;
- Telegram live not connected;
- eBay live not connected.

These are intentionally blocked/stubbed until Windows/server/env gates.

### 8. n8n draft
Created:
- `workflows/n8n_listing_pipeline_v1.json`

Status:
- draft only;
- not imported;
- not active.

## Important remembered server facts
Server runtime already existed and must not be overwritten blindly:
- server path: `/home/ionlipca7/runtime_eco_v1`
- Telegram/runtime bridge existed by memory;
- eBay token refresh/guard previously worked;
- eBay readonly verification previously worked;
- Inventory API photo update route technically worked;
- live listing `318228151138` exists; price `10.99`, quantity `40` must stay unchanged;
- live listing `318222589463` / UD24 exists and was verified;
- server may contain V3/V4/V5 temporary photo artifacts.

Server must only be touched after Windows local PASS.

## What is not completed by design
Not completed yet because it requires Windows/server/env/live gates:
- real image provider integration;
- Canva editable route;
- Telegram live send/receive;
- n8n active workflow import;
- eBay live runtime;
- server deployment;
- server cleanup/delete.

## Immediate next step in new chat
Start with Windows local check only.

Where:
- WINDOWS CMD

Exact path:
- `D:\ECOM_LISTING_AGENT_MVP`

Command:
```cmd
cd /d D:\ECOM_LISTING_AGENT_MVP
set PYTHONIOENCODING=utf-8
storage\tools\ecom_os_v3\run_full_local_check_v1.bat
```

## What operator must send back
After command finishes, send:
1. full CMD output;
2. `storage\tools\ecom_os_v3\security_secrets_guard_result_v1.json`
3. `storage\tools\ecom_os_v3\package_audit_result_v1.json`
4. `storage\tools\ecom_os_v3\bootstrap_verify_local_package_result_v1.json`
5. latest `storage\outputs\ecom_os_v3\e2e_virtual\<RUN_ID>\02_e2e_final_report.json`
6. latest `storage\outputs\ecom_os_v3\portfolio_strategy\<RUN_ID>\07_portfolio_strategy_summary.json`

## If blocked
Do not jump to server.
Fix only exact blocker, rerun Windows full local check.

## If pass
Next route:
1. server readonly diff audit;
2. deploy filter;
3. merge manifest;
4. operator approval;
5. deploy approved blocks only;
6. runtime verify;
7. later Telegram/n8n/eBay gates.

## STOP rule
This chat ended at:
- `FINISH_GITHUB_PREPARATION_V4`
- `STOP`

New chat must begin at:
- `RUN_WINDOWS_FULL_LOCAL_CHECK_V1`
