# 42_FINANCE_EXPORT_AND_TAX_ARCHIVE_ARCHITECTURE_V1

Status: FINANCE_TAX_ARCHIVE_ARCHITECTURE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the finance export and tax archive architecture for ECOM OS.

This layer prepares marketplace sales, purchase costs, fees, payouts, receipts, and tax-relevant documents for later accounting/export workflows.

## External practice alignment
This strategy follows:
- German ELSTER electronic tax submission workflows;
- VAT/preliminary VAT return preparation;
- DATEV/e-commerce accounting import patterns;
- marketplace payout reconciliation;
- invoice/receipt linkage;
- document retention governance;
- audit-safe financial event history.

## Core decision
Finance layer records and exports financial evidence.
It must not publish listings, mutate inventory, or change marketplace state.

Correct route:

```text
Commerce Events
 -> Finance Event Normalizer
 -> Receipt/Invoice Archive Link
 -> Payout/Fee Reconciliation
 -> Export Package
 -> Operator/Tax Advisor Review
```

Forbidden route:

```text
Finance Layer -> Marketplace Live Action
```

## Finance event model
Important finance events:
- purchase_recorded;
- purchase_receipt_attached;
- stock_received;
- order_created;
- order_paid;
- marketplace_fee_recorded;
- ad_fee_recorded;
- shipping_cost_recorded;
- payout_received;
- refund_processed;
- return_received;
- tax_export_generated.

## Required fields
Each finance event should include:
- event_id;
- event_type;
- timestamp;
- marketplace;
- internal_sku;
- order_id optional;
- transaction_id optional;
- gross_amount;
- fee_amount;
- shipping_amount;
- tax_amount if known;
- net_amount;
- currency;
- document_refs;
- audit_source;
- operator_notes.

## Purchase cost tracking
For every purchased item/batch:
- supplier name;
- supplier country;
- purchase date;
- purchase price;
- shipping/import cost;
- quantity purchased;
- receipt/invoice reference;
- landed cost per unit;
- allocated bundle component cost.

## Marketplace payout reconciliation
Reconcile:
- marketplace orders;
- marketplace fees;
- payment processor payouts;
- refunds;
- chargebacks if applicable;
- ad charges;
- shipping labels;
- bank account deposits.

Goal:

```text
order revenue - fees - refunds - ads - shipping = payout reconciliation basis
```

## Document archive
Archive references should support:
- supplier receipts;
- marketplace invoices;
- payout reports;
- shipping receipts;
- return/refund documents;
- ad invoices;
- tax export packages.

Documents should be linked by event_id / order_id / internal_sku.

## Export targets
Future export targets:
- ELSTER-preparation summaries;
- DATEV-compatible exports;
- CSV for tax advisor;
- Storeroboter-style archive/export package;
- marketplace-specific payout reports;
- VAT summary reports.

## Separation from tax filing
ECOM OS may prepare export packages.
It should not claim to replace a tax advisor or automatically file tax returns without explicit future legal/accounting review.

## Multi-marketplace normalization
All marketplaces must normalize into the same finance event model.

Examples:
- eBay sale -> finance event;
- Amazon sale -> finance event;
- Etsy sale -> finance event.

Marketplace-specific fee structures stay in adapter/export mapping.

## Inventory integration
Finance layer reads inventory cost basis.
It must not mutate stock.

Inventory cost basis must support:
- single SKU;
- variant SKU;
- bundle component allocation;
- returned goods status;
- damaged stock status.

## Operator review
Operator should see Russian summary:
- sales total;
- fees total;
- ads total;
- refunds total;
- estimated profit;
- missing receipts;
- unreconciled payouts;
- export readiness.

## STOP conditions
STOP if:
- finance layer attempts live marketplace action;
- tax filing is attempted automatically;
- receipt/invoice source is missing for purchase cost;
- payout does not reconcile;
- VAT/tax category is unclear;
- export would include secrets/tokens;
- document archive links are missing.

STOP: This document defines finance/tax archive architecture only. It does not file tax returns, generate legal advice, or execute marketplace actions.
