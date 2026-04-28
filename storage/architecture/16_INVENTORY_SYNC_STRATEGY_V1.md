# 16_INVENTORY_SYNC_STRATEGY_V1

Status: DRAFT_STRATEGY_ONLY
Branch: architecture-audit-v1

## Purpose
Prevent overselling and inventory inconsistency across multiple marketplaces, bundles, kits, and quantity variants.

## Core principle
Inventory must exist as one central truth inside Inventory Sales Core.
Marketplaces do not own inventory truth.

## Central inventory flow

```text
Purchase/Supplier Data
  -> Inventory Sales Core
  -> Reservation Logic
  -> Marketplace Quantity Sync
  -> Sales Event
  -> Inventory Update
  -> Marketplace Re-sync
  -> Verify Consistency
```

## Inventory states
- total_quantity
- available_quantity
- reserved_quantity
- sold_quantity
- damaged_quantity
- incoming_quantity

## Reservation logic
When an order is detected:
1. Reserve stock immediately.
2. Prevent duplicate sale.
3. Update all marketplace availability.
4. Verify marketplace update success.

## Bundle logic
Example:
Bundle A:
- 2 cables
- 1 charger

When bundle sells:
- cable inventory decreases by 2
- charger inventory decreases by 1
- related listings may require quantity recalculation

## Variation logic
Variation-level stock must be tracked separately:
- black 1m cable
- black 2m cable
- white 1m cable

Each variation may have:
- own SKU
- own quantity
- own images
- own marketplace mapping

## Marketplace synchronization

### eBay
- quantity updates
- listing stop when quantity = 0 if required
- variation-level quantity sync
- bundle-safe updates

### Amazon future
- seller inventory feed/API sync
- parent-child stock awareness
- FBA/FBM distinction

## Sync safety rules
- No marketplace may update inventory directly without Inventory Sales Core.
- Inventory sync failures must trigger warning state.
- Live quantity updates require verify-after-update.
- Marketplace API success is not enough.
- Brain must track stale sync state.

## Telegram operator notifications
Examples:
- "остаток товара почти закончился"
- "bundle inventory mismatch"
- "quantity sync failed on eBay"
- "Amazon stock differs from central inventory"

## Future upgrades
- auto reorder recommendation
- supplier lead-time prediction
- seasonal inventory logic
- dead stock detection
- sales velocity prediction

FINISH: Inventory synchronization strategy defined.
STOP: No runtime synchronization from this file.
