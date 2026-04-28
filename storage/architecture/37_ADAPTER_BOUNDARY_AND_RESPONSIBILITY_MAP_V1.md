# 37_ADAPTER_BOUNDARY_AND_RESPONSIBILITY_MAP_V1

Status: ADAPTER_BOUNDARY_MAP
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the exact boundary between Brain Governance Core and Marketplace Adapters.

This prevents a future multi-marketplace monolith and keeps eBay, Amazon, Etsy, Shopify, Kaufland, Otto, and future marketplaces isolated.

## External practice alignment
This map follows:
- Ports and Adapters / Hexagonal Architecture;
- Bounded Contexts;
- Anti-Corruption Layer;
- Separation of Concerns;
- Least Privilege;
- Fail Secure;
- Policy Enforcement / Gateway patterns.

## Core decision
Brain owns governance.
Adapters own marketplace translation and execution details.

Brain must not contain marketplace API quirks.
Adapters must not own global governance.

---

# 1. Brain responsibilities

Brain owns:
- policy enforcement;
- approval checks;
- environment checks;
- forbidden path checks;
- verify-before-advance checks;
- audit decision writing;
- operator-facing governance messages;
- route decision: ALLOW / BLOCK / CHECK_REQUIRED / ALLOW_DRY_RUN_ONLY.

Brain does NOT own:
- eBay API payload shape;
- Amazon schema mapping;
- marketplace retry implementation;
- marketplace-specific error parsing;
- inventory truth;
- direct publish execution.

---

# 2. Adapter responsibilities

Each marketplace adapter owns:
- marketplace-specific schema mapping;
- marketplace-specific payload building;
- marketplace API client behavior;
- marketplace-specific retry/backoff rules;
- marketplace-specific error classification;
- marketplace-specific visibility/read verification implementation;
- marketplace-specific category/attribute rules.

Adapters do NOT own:
- approval policy;
- global inventory truth;
- operator permissions;
- Brain route decisions;
- cross-marketplace governance.

---

# 3. Inventory ownership

Inventory Sales Core is the single source of truth.

Adapters consume inventory state and report marketplace state back.

Forbidden:

```text
marketplace adapter owns central inventory truth
```

Reason:
- prevents overselling;
- prevents quantity drift;
- protects multi-marketplace synchronization.

---

# 4. Verification ownership

Adapter owns:
- how to verify marketplace result.

Brain owns:
- whether verification is required before route advancement.

Example:

```text
Adapter: eBay active listing visibility check
Brain: route cannot advance until visibility check result exists
```

---

# 5. Retry ownership

Adapter owns:
- marketplace-specific retry and backoff.

Brain owns:
- whether retry is allowed under governance.

Forbidden:

```text
adapter retries dangerous action without Brain-approved retry policy
```

---

# 6. Audit ownership

Brain owns:
- governance decision audit.

Adapter owns:
- marketplace call result audit.

Archive/Audit layer owns:
- long-term combined timeline.

---

# 7. Future marketplace rule

New marketplace = new adapter.

Allowed:

```text
Brain -> Amazon Adapter -> Amazon API
Brain -> eBay Adapter -> eBay API
Brain -> Etsy Adapter -> Etsy API
```

Forbidden:

```text
one giant marketplace_runtime.py with all marketplace logic mixed together
```

---

# 8. Adapter contract

Every adapter must expose a stable contract:

```json
{
  "marketplace": "ebay",
  "capabilities": [],
  "supports_read_only": true,
  "supports_live": false,
  "requires_approval": true,
  "requires_verification": true
}
```

---

# 9. First integration rule

First adapter integration must be read-only.

Allowed first target:
- active listings read-only verify;
- token health read-only verify;
- draft validation;
- category/attribute read-only check.

Forbidden first target:
- publish;
- revise;
- delete;
- inventory mutation;
- ad activation;
- offer sending.

---

# 10. STOP conditions

STOP if:
- Brain imports marketplace API client;
- adapter imports operator approval UI directly;
- adapter owns central inventory truth;
- adapter contains global governance logic;
- marketplace-specific code leaks into Universal Product Model;
- live execution becomes reachable before read-only integration passes.

STOP: This document defines adapter boundaries only. It does not authorize live integration.
