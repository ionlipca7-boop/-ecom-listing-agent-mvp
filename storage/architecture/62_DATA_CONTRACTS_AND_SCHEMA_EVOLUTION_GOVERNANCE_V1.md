# 62_DATA_CONTRACTS_AND_SCHEMA_EVOLUTION_GOVERNANCE_V1

Status: DATA_CONTRACT_SCHEMA_EVOLUTION_GOVERNANCE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define data contracts and schema evolution governance for ECOM OS.

## External practice alignment
This strategy follows:
- data contract governance;
- backward compatibility;
- schema versioning;
- replay compatibility;
- controlled rollout of producers/consumers;
- explicit semantic versioning.

## Core decision
Schemas are contracts. Contracts must evolve safely.

## Contracted data models
Contracts required for:
- action_request;
- Brain decision audit;
- event timeline;
- inventory event;
- finance event;
- marketplace adapter capabilities;
- AI listing candidate;
- approval state;
- recovery state.

## Versioning rules
Every durable schema should include:
- schema_name;
- schema_version;
- created_at or event timestamp;
- compatibility notes where needed.

## Safe schema changes
Allowed:
- add optional fields;
- add fields with defaults;
- extend enum only with compatibility mapping;
- add new event type version;
- keep aliases for renamed fields during transition.

## Breaking schema changes
Breaking:
- remove required field;
- rename field without alias;
- change field meaning silently;
- change type without migration;
- change timestamp semantics;
- reuse old event name with new meaning.

## Replay compatibility
Historical events must remain interpretable.

If meaning changes:
- create new event version;
- write migration notes;
- preserve old reader compatibility;
- test replay.

## Deployment order
For compatible schema rollout:
1. update consumers/readers first;
2. support old and new versions;
3. update producers/writers;
4. observe;
5. deprecate old fields later.

## STOP conditions
STOP if:
- schema change breaks replay;
- old events become unreadable;
- finance/inventory meaning changes silently;
- required field removed without migration;
- version missing for durable event.

STOP: This document defines schema governance only.
