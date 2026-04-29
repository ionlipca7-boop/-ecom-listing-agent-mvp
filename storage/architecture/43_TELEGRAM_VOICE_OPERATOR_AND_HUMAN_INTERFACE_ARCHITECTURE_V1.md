# 43_TELEGRAM_VOICE_OPERATOR_AND_HUMAN_INTERFACE_ARCHITECTURE_V1

Status: TELEGRAM_VOICE_OPERATOR_ARCHITECTURE
Branch: feature/brain-hard-gate-dry-run-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the Telegram, voice, and human operator interface architecture for ECOM OS.

This layer lets the operator control the system in Russian through text/voice while preserving Brain governance, approval gates, audit trails, and safety boundaries.

## External practice alignment
This strategy follows:
- human-in-the-loop approval workflows;
- approval queue pattern;
- conversational UI best practices;
- risk-based confirmations;
- auditability and accountability;
- agent governance and explicit permissions;
- fail-secure operator interaction.

## Core decision
Telegram/Voice is an interface layer, not an execution owner.

Correct route:

```text
Operator Text/Voice
 -> Telegram Interface
 -> Intent Normalizer
 -> Brain Governance
 -> Approval Queue / Decision
 -> Adapter or Module
 -> Verify
 -> Audit
 -> Russian Response
```

Forbidden route:

```text
Telegram/Voice -> Direct Marketplace Live Action
```

## Interface responsibilities
Telegram/Voice layer owns:
- Russian operator messages;
- command intake;
- voice-to-text normalized intent;
- approval buttons;
- status notifications;
- preview delivery;
- error/status explanation;
- operator context.

Telegram/Voice layer does not own:
- marketplace execution;
- inventory truth;
- approval policy;
- marketplace payload construction;
- live action authorization;
- finance/tax decisions.

## Intent normalization
Voice/text input must be normalized into structured action requests.

Example:

Operator says:

```text
Проверь этот листинг и подготовь к публикации
```

Normalized request:

```json
{
  "requested_action": "prepare_listing_review_v1",
  "requested_by": "telegram",
  "environment": "TELEGRAM_INTERFACE",
  "target_module": "listing_review",
  "risk_level": "draft",
  "requires_verification": true
}
```

## Approval queue pattern
High-risk actions must pause and wait for explicit operator approval.

Examples requiring approval:
- publish listing;
- revise live listing;
- delete/end listing;
- send offer;
- enable ads;
- price change;
- inventory mutation;
- finance export finalization.

Approval message must include:
- action name;
- listing/product target;
- risk level;
- expected result;
- margin/price impact if relevant;
- verification requirement;
- approve/reject/edit options.

## Risk-based confirmation
Low risk:
- status check;
- draft generation;
- read-only verification.

Medium risk:
- draft content changes;
- price recommendation;
- ad recommendation.

High risk:
- publish;
- revise;
- delete/end;
- offer sending;
- ad enablement;
- inventory quantity changes.

High risk requires explicit approval and audit.

## Operator language rules
Operator-facing output must be:
- Russian by default;
- short;
- clear;
- action-oriented;
- no raw stack traces;
- no secrets/tokens;
- include whether live action happened or not.

German content preview is allowed for listings, but explanation remains Russian.

## Voice command safety
Voice commands must not directly trigger high-risk action.

Voice flow:

```text
voice command
 -> transcript
 -> intent normalization
 -> Brain check
 -> confirmation prompt if risky
 -> approval button/text
 -> execution only after approval
```

Misheard voice commands must become CHECK_REQUIRED.

## Audit requirements
Every operator decision must record:
- requested action;
- normalized intent;
- operator identity/source;
- approval or rejection;
- timestamp;
- Brain decision;
- resulting verification state.

## Notification types
Telegram should notify:
- draft ready;
- approval needed;
- action blocked;
- verification required;
- marketplace result verified;
- inventory risk;
- finance missing receipt;
- recovery needed;
- system health warning.

## Human override
Operator can reject or override AI recommendation.

Override must be recorded with:
- operator decision;
- reason optional;
- affected product/listing;
- timestamp.

## STOP conditions
STOP if:
- Telegram directly calls marketplace live adapter;
- voice command triggers live action without confirmation;
- approval state is missing for high-risk action;
- operator message contains secrets;
- normalized intent is ambiguous;
- Brain decision is bypassed;
- audit cannot be written.

STOP: This document defines Telegram/Voice operator architecture only. It does not execute Telegram runtime changes or live marketplace actions.
