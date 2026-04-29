# 38_UNIVERSAL_PRODUCT_MODEL_AND_INVENTORY_CORE_V1

Status: PRODUCT_INVENTORY_CORE_STRATEGY
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the universal product model and inventory core strategy for ECOM OS.

This prepares the system for eBay now, Amazon later, and future marketplaces without creating a marketplace-specific monolith.

## External practice alignment
This strategy follows:
- centralized inventory as single source of truth;
- SKU normalization;
- real-time/event-driven inventory updates;
- safety buffers for oversell prevention;
- marketplace-independent domain model;
- adapter-based marketplace translation.

## Core principle
Product, listing, inventory, and marketplace payload are different concepts.

```text
Product != Listing
Listing != Inventory
Marketplace Payload != Product Core
```

## Universal Product Model ownership
Universal Product Model owns:
- internal product identity;
- supplier data;
- base attributes;
- normalized SKU family;
- variants;
- bundle definitions;
- media references;
- content inputs;
- marketplace payload slots.

It must not own:
- eBay API-specific payload logic;
- Amazon schema-specific behavior;
- live inventory mutation;
- marketplace retry behavior.

## Inventory Sales Core ownership
Inventory Sales Core owns:
- quantity_total;
- quantity_available;
- quantity_reserved;
- quantity_sold;
- quantity_damaged;
- quantity_incoming;
- stock movements;
- reservations;
- bundle component deductions;
- oversell protection;
- channel visibility rules.

Inventory Sales Core is the single source of truth.

## SKU governance
Every sellable unit must have:
- internal_sku;
- supplier_sku optional;
- marketplace_sku mapping optional;
- variant attributes optional;
- bundle component mapping optional.

Marketplace SKUs are mappings, not the master identity.

## Variant model
Variants may include:
- color;
- size;
- length;
- material;
- pack quantity;
- style;
- marketplace-specific variation theme mapping.

Variant stock must be tracked separately.

## Bundle model
Bundles/kits must reference component SKUs.

Example:

```json
{
  "bundle_sku": "KIT-CABLE-CHARGER-001",
  "components": [
    {"internal_sku": "CABLE-001", "quantity": 2},
    {"internal_sku": "CHARGER-001", "quantity": 1}
  ]
}
```

When bundle sells, component inventory must be reduced centrally.

## Marketplace payload boundary
Adapters translate universal model into marketplace payloads.

```text
Universal Product Model
 -> eBay Adapter Payload
 -> Amazon Adapter Payload
 -> Future Adapter Payload
```

The universal model stays marketplace-neutral.

## Channel visibility rules
Actual inventory and visible marketplace inventory may differ.

Examples:
- actual stock: 10;
- eBay visible: 8;
- Amazon visible: 7;
- reserved safety buffer: 2.

Reason:
- prevent overselling;
- handle sync latency;
- prioritize higher-margin channels;
- protect account health.

## Event-driven inventory logic
Important events:
- purchase_received;
- stock_reserved;
- order_created;
- order_cancelled;
- return_received;
- bundle_sold;
- marketplace_sync_failed;
- stock_reconciled.

Each event should update central inventory before marketplace sync.

## AI listing inputs
Universal model should provide AI listing generation with:
- product facts;
- compatibility;
- use cases;
- variant attributes;
- bundle structure;
- photos;
- market research;
- price constraints;
- marketplace restrictions.

AI content generation must not mutate inventory.

## Oversell prevention rules
Stop if:
- quantity_available <= 0;
- bundle component stock insufficient;
- marketplace quantity differs from central inventory and cannot be reconciled;
- sync status is stale for high-velocity product;
- safety buffer would be violated.

## Future integration rule
Before Amazon or another marketplace is added, it must consume the Universal Product Model and Inventory Sales Core through adapters.

Forbidden:

```text
Amazon adapter creates separate inventory truth
```

## STOP conditions
STOP architecture/integration if:
- product model becomes eBay-specific;
- marketplace adapter owns central inventory;
- bundle deduction bypasses inventory core;
- variants share one unsafe stock bucket;
- AI listing generation mutates stock;
- channel sync bypasses Brain governance.

STOP: This document defines product/inventory architecture only. It does not execute inventory sync or live marketplace actions.
