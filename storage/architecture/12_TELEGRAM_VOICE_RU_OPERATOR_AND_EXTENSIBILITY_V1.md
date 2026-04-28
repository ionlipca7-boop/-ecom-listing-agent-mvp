# 12_TELEGRAM_VOICE_RU_OPERATOR_AND_EXTENSIBILITY_V1

Status: DRAFT_STRATEGY_ONLY
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Publish called: false

## Purpose
Define the future Telegram operator experience: Russian-first conversational control, voice input, safe intent parsing, and non-breaking extensibility for future upgrades.

## Operator requirement
The operator should be able to control the system through Telegram in natural Russian, including voice messages, not only typed commands.

Examples:
- "проверь этот листинг"
- "почему товар не продается"
- "посмотри конкурентов"
- "сделай описание лучше"
- "отправь скидку 5 процентов, если можно"
- "проверь остатки"
- "подготовь листинг, но не публикуй"

## Required blocks

### operator_language_layer
Role:
- Understand Russian operator messages.
- Convert free text into structured intent.
- Preserve operator language as Russian.
- Ask clarification when the command is ambiguous or risky.

### voice_input_layer
Role:
- Receive Telegram voice message.
- Transcribe speech to Russian text.
- Send text to operator_language_layer.
- Store transcript for audit.

### intent_safety_layer
Role:
- Classify intent as read-only, draft, approval, live action, dangerous action.
- Block live action unless approval gate is open.
- Never convert unclear speech directly into publish/revise/delete.

### russian_response_layer
Role:
- Return all operator-facing messages in Russian.
- Summarize technical errors in understandable Russian.
- Keep German only for customer-facing marketplace listing content.

## Structured intent example

```json
{
  "operator_language": "ru",
  "raw_message": "проверь этот листинг",
  "intent": "verify_listing",
  "risk_level": "read_only",
  "requires_approval": false,
  "target": {
    "listing_id": null,
    "draft_id": null
  },
  "next_step": "ask_for_target_or_use_current_pointer"
}
```

## Safety rules
- Russian voice/text can start analysis.
- Russian voice/text can prepare drafts.
- Russian voice/text cannot trigger publish without explicit approval confirmation.
- Dangerous actions require typed or button confirmation, not voice-only.
- If speech recognition is uncertain, system must ask confirmation.

## Future-proof upgrade principle

### capability_registry_block
The system must track available modules and capabilities:

```json
{
  "module": "ebay_adapter",
  "capabilities": ["publish", "verify", "send_offer", "promoted_listing"],
  "status": "stable_or_draft",
  "requires_approval": true
}
```

### plugin_adapter_policy
New capabilities should be added as blocks/adapters, not by rewriting core logic.

Future additions may include:
- Amazon adapter
- new marketplace adapter
- new AI model
- new photo processor
- finance connector
- n8n workflow
- agent runner
- advertising automation

## Non-breaking upgrade rules
- New module must declare capabilities.
- New module must declare input/output contract.
- New module must declare risk level.
- New module must pass dry-run before live use.
- New module must not bypass Brain.
- New module must not bypass Approval Gate.
- New module must not write into main without review.

## Recommended implementation order
A. Finish architecture audit.
B. Define capability registry schema.
C. Define Russian intent schema.
D. Add Telegram text-intent parser.
E. Add voice transcription later.
F. Add button confirmation for risky actions.
G. Add marketplace/agent/plugin capability registration.
FINISH. Review before implementation.
STOP. No live action from this file.
