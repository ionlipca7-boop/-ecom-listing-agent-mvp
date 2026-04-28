# 19_ARCHITECTURE_CONSOLIDATION_AUDIT_V1

Status: CONSOLIDATION_REVIEW
Branch: architecture-audit-v1
Base: main

## Safety verification
- Main branch was not changed.
- Server runtime was not touched.
- No publish, revise, delete, or live marketplace action was called.
- All audit additions are under storage/architecture/.
- Existing runtime/source files were not modified.

## GitHub branch result
The branch architecture-audit-v1 is ahead of main with audit-only architecture documents. It is not behind main at the time of this check.

## External practice check
The current direction is aligned with common practices:
- Use focused ADRs for important architecture decisions.
- Use one central inventory source of truth for multi-channel selling.
- Avoid a full rewrite when the current system can be evolved in stages.
- Consolidate broad ideas into phases before implementation.

## Duplicate and overlap review
Some overlap exists, but it is acceptable as audit material. Implementation must consolidate it.

### Vision overlap
Files 08, 09, and 10 overlap around upgrades and marketplace future.
Decision: keep 10 as master backlog, 09 as marketplace strategy, 08 as priority queue.

### Product model overlap
Files 11, 14, and 17 overlap around variants, AI search, and quality.
Decision: 14 Universal Product Model becomes the data core; 11 and 17 become extensions/gates.

### Control overlap
Files 04, 13, and 15 overlap around boundaries, capabilities, and validation.
Decision: 04 defines boundaries, 13 defines module capabilities, 15 defines marketplace validation.

### Inventory overlap
Files 14 and 16 overlap around stock.
Decision: Inventory Sales Core is the single source of truth; marketplace adapters mirror stock only.

## Stop-expansion rule
No more broad meta-layer documents now. The architecture is large enough for first execution planning.

Allowed next documents only:
1. FINAL_MODULE_MAP_V1.md
2. CORE_VS_FUTURE_MATRIX_V1.md
3. MVP_EXECUTION_ORDER_V1.md
4. DEPENDENCY_GRAPH_V1.md
5. IMPLEMENTATION_ROADMAP_V1.md
6. Focused ADR files only when a real decision must be recorded.

## Core MVP boundary
First working system should focus on:
- Brain / Orchestrator
- Russian Telegram operator layer
- Universal Product Model
- eBay adapter with real visibility verify
- Inventory Sales Core
- Approval Gate
- Marketplace Validation Rules
- Quality Score
- Basic competitor and price intelligence
- Variant and bundle support draft
- Recovery playbooks
- Audit and memory

## Future, not MVP
- Amazon live adapter
- n8n orchestration
- multi-agent runner
- predictive analytics
- knowledge graph
- distributed runtime
- full finance/tax system

## Main risk
The main risk is not missing ideas anymore. The main risk is overexpansion. The next phase must convert the audit into an executable map.

## Correct next action
Create FINAL_MODULE_MAP_V1 and CORE_VS_FUTURE_MATRIX_V1, then stop architecture expansion and move to implementation planning.
