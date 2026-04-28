# 04_BLOCK_BOUNDARIES_V1

Status: DRAFT
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Core boundary rule
No operational block should directly command another operational block. All execution must go through Brain / Orchestrator.

Correct flow:

```text
Operator / Telegram / Chat
  -> Operator Language Layer
  -> Brain / Orchestrator
  -> State / Rules / Approval Gate
  -> Target Block
  -> Result / Verify
  -> Archive / Telegram Response
```

## Blocks and boundaries

### 00_brain_orchestrator
Owns:
- next_allowed_action
- route control
- safety gates
- environment decision
- module dispatch

Must not:
- contain marketplace-specific payload details
- store secrets
- bypass approval

### 01_operator_language_and_telegram
Owns:
- Russian operator interface
- voice/text message intake
- intent parsing
- Telegram responses

Must not:
- publish directly
- revise directly
- delete directly
- access secrets directly

### 02_universal_listing_core
Owns:
- neutral product/listing model
- German listing content
- HTML/template intent
- item facts
- quality score input

Must not:
- call eBay/Amazon directly
- assume one marketplace only

### 03_photo_engine
Owns:
- image count
- image quality gate
- hero image selection
- marketplace photo readiness

Must not:
- publish listing
- decide final price

### 04_price_market_research
Owns:
- competitor scan
- price range
- target/min/aggressive price
- market demand notes

Must not:
- change active marketplace price without approval

### 05_inventory_sales_core
Owns:
- supplier purchase data
- quantity available/reserved/sold
- bundle component stock
- sales channel sync model
- oversell protection

Must not:
- auto-delete marketplace listings
- change marketplace quantity without Brain approval path

### 06_marketplace_adapter_layer
Owns:
- eBay adapter
- Amazon adapter future
- marketplace payload mapping
- marketplace validation
- publish/verify interface

Must not:
- own universal listing logic
- bypass approval
- treat API success as business success

### 07_offers_ads_strategy
Owns:
- eBay send offers to interested buyers strategy
- promoted listing recommendations
- ad rate logic
- offer/discount guard

Must not:
- send live offers or ads without approval gate

### 08_approval_gate
Owns:
- draft approval
- publish approval
- revise approval
- delete approval
- offer/ad approval

Must not:
- create content or call marketplace directly

### 09_archive_memory_audit
Owns:
- transition files
- ADR
- error history
- listing timeline
- audit logs

Must not:
- be treated as current state when pointer says otherwise

### 10_server_runtime
Owns:
- env/secrets
- runtime execution
- Telegram process
- scheduled jobs

Must not:
- be touched from GitHub audit branch
- print secrets

### 11_github_sync
Owns:
- branches
- source audit
- PR/review path

Must not:
- represent live eBay/server truth alone

### 12_finance_connector
Owns:
- export sales/purchase/fee data
- archive references
- connection to separate finance/tax system

Must not:
- become full tax engine inside ECOM OS core

## Cross-block contracts
Every block must declare:
- input schema
- output schema
- risk level
- read/write permissions
- dry-run capability
- live capability status

## Forbidden direct paths
- Telegram -> eBay publish
- Listing Builder -> eBay publish
- Price Engine -> marketplace revise
- Ads Engine -> live campaign start
- Archive -> live action
- GitHub audit -> server runtime
- Any block -> secrets print

## Required verification paths
- publish response -> real visibility verify
- quantity update -> inventory consistency verify
- bundle sale -> component stock verify
- promotion/offer -> margin verify
- Amazon listing -> product type schema validation
- eBay variation -> category variation support validation

FINISH: Boundaries defined.
STOP: No runtime changes.
