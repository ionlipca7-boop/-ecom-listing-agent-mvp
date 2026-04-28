# 70_ARCHITECTURE_DECISION_LOG_AND_ADR_CLOSURE_V1

Status: ADR_CLOSURE_GOVERNANCE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Close the architecture expansion phase by defining the decision log and ADR governance needed before implementation transition.

## External practice alignment
This strategy follows:
- Architecture Decision Records;
- one decision per record;
- clear ADR status;
- timestamped/versioned decisions;
- rejected alternatives;
- ADRs stored with code;
- supersede instead of silently rewriting history.

## Core decision
The architecture is now broad enough. New work should become focused ADRs or implementation tasks, not more broad meta-documents.

## ADR statuses
Allowed statuses:
- PROPOSED;
- ACCEPTED;
- DEPRECATED;
- SUPERSEDED.

## Required ADR format
Each ADR should include:
- title;
- status;
- context;
- decision;
- alternatives considered;
- consequences;
- links to related architecture docs;
- date/version.

## Candidate ADRs
Initial ADRs should cover:
- Brain is governance, not execution;
- Inventory Sales Core is single source of truth;
- Marketplace adapters isolate external APIs;
- AI generates candidates, not marketplace state;
- No live action without approval and verification;
- Secrets are runtime assets, not source-code assets;
- Capability enablement must be progressive.

## Stop-expansion rule
No more broad architecture expansion unless a real gap blocks implementation.

Allowed after this:
- focused ADR;
- implementation task;
- dry-run test;
- integration checklist;
- production readiness evidence.

## STOP conditions
STOP if:
- architecture docs continue expanding without implementation need;
- ADR combines multiple unrelated decisions;
- old decision is silently rewritten;
- implementation starts without accepted decisions for high-risk areas.

STOP: This document defines ADR closure governance only.
