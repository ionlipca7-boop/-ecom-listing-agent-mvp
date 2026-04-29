# 54_OPERATOR_CONTROL_ROOM_AND_GLOBAL_DASHBOARD_ARCHITECTURE_V1

Status: CONTROL_ROOM_DASHBOARD_ARCHITECTURE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the operator control room and global dashboard architecture for ECOM OS.

## External practice alignment
This strategy follows:
- observability-first systems;
- OpenTelemetry-style telemetry separation;
- logs/metrics/traces visibility;
- SRE dashboard best practices;
- environment-aware monitoring.

## Core decision
The control room is the operator visibility layer, not a hidden execution engine.

## Dashboard domains
Dashboard should expose:
- system health;
- marketplace health;
- inventory health;
- route queue status;
- approval queue;
- recovery alerts;
- finance/export alerts;
- degraded mode status;
- audit/event stream;
- agent orchestration status.

## Telemetry model
The system should correlate:
- logs;
- metrics;
- traces;
- events;
- approvals;
- recovery actions.

## Environment visibility
Dashboard must separate:
- LOCAL_DEV;
- TEST;
- DRY_RUN;
- PRODUCTION.

## Operator UX rules
Operator output should be:
- Russian-first;
- concise;
- action-oriented;
- risk-aware;
- verification-aware.

## STOP conditions
STOP if:
- dashboard exposes secrets;
- production and test are mixed visually;
- alert severity is unclear;
- audit/events cannot be correlated.

STOP: This document defines control room/dashboard architecture only.
