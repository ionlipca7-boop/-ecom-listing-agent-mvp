# 36_READ_ONLY_INTEGRATION_STRATEGY_V1

Status: READ_ONLY_INTEGRATION_STRATEGY
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the first safe integration strategy between the Brain governance layer and the existing ECOM OS runtime.

The first integration phase must remain read-only.

## Internet-aligned architecture principles
This strategy follows:
- Secure by Design;
- Adapter architecture;
- Explicit trust boundaries;
- Fail secure behavior;
- Least privilege;
- Incremental modernization.

## Core integration principle
Brain must not directly own marketplace execution.

Correct route:

```text
Telegram / Voice / UI
        ↓
Interface Layer
        ↓
Brain Governance Layer
        ↓
Marketplace Adapter
        ↓
Marketplace API
```

Forbidden route:

```text
Telegram -> Marketplace live
```

## First integration scope
Allowed first integration:

```text
Brain evaluates request
→ Brain returns governance decision
→ Existing runtime remains read-only
```

Not allowed in first integration:
- publish;
- revise;
- delete;
- inventory mutation;
- ad enable/disable;
- offer sending;
- server runtime restart.

## Read-only route wrapping
Initial target routes:
- read-only inventory verify;
- read-only active listings verify;
- read-only token health verify;
- read-only draft validation.

Integration logic:

```text
Request
 -> Brain check
 -> existing read-only route
 -> verification
 -> audit
```

## Marketplace adapter isolation
Each marketplace must have:
- isolated adapter;
- marketplace-specific logic;
- marketplace-specific schema mapping;
- marketplace-specific retry rules.

Shared governance remains inside Brain.

## Inventory governance strategy
Inventory becomes:

```text
single source of truth
```

Marketplace adapters consume inventory state.

## Telegram / voice governance flow
Future flow:

```text
Voice/Text
 -> Telegram interface
 -> Brain governance
 -> Adapter route
```

Telegram interface must remain:
- non-live by default;
- approval-aware;
- audit-aware;
- verification-aware.

## Read-only integration rules
PASS only if:
- Brain decision exists before route execution;
- Brain audit exists;
- no live flags become true;
- existing runtime files remain unchanged;
- adapter remains isolated;
- verification remains required.

FAIL if:
- Brain bypass appears;
- Telegram direct execution appears;
- adapter mutates inventory directly;
- publish/revise/delete becomes reachable.

## Future expansion path
Future marketplaces:
- eBay
- Amazon
- Etsy
- Shopify
- Kaufland
- Otto

All future capabilities should remain:

```text
governed
modular
adapter-based
```

## STOP conditions
STOP integration immediately if:
- Brain starts directly executing live routes;
- Telegram bypass appears;
- inventory truth splits;
- adapter contains governance logic;
- existing runtime becomes tightly coupled to Brain.

## Next phase after approval
After read-only integration review PASS:
1. connect Brain to one read-only route only;
2. verify deterministic behavior;
3. verify audit output;
4. verify no side effects;
5. review integration result;
6. only then discuss limited live governance.

STOP: This strategy defines read-only integration only. It does not authorize live integration.
