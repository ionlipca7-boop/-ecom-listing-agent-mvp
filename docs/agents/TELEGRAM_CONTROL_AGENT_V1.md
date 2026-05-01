# TELEGRAM_CONTROL_AGENT_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Make Telegram the Russian operator control panel for the ECOM OS V3 listing pipeline.

Telegram must not be a blind executor. It is a controlled review, command, preview, and approval interface.

## Operator Language
Default operator language: Russian.

Telegram must:
- understand Russian text
- accept Russian voice notes after transcription
- reply in Russian
- produce German marketplace output for eBay Germany

## Inputs
- Russian text command
- Russian voice note
- product URL
- product screenshots
- real product photos
- approve/reject/rework commands

## Outputs
- Product Passport preview
- photo pack preview
- title options preview
- item specifics preview
- HTML preview
- critic PASS/BLOCKED report
- approval packet

## Command Classes

### Intake commands
Examples:
- "сделай листинг по этой ссылке"
- "вот фото товара"
- "сделай 8 фото"
- "сделай немецкий title"

### Rework commands
Examples:
- "сделай другие фото"
- "первое фото без текста"
- "поменяй title"
- "сделай описание короче"
- "убери английский"
- "только немецкий"

### Preview commands
Examples:
- "покажи 8 фото"
- "покажи title"
- "покажи HTML"
- "покажи что будет опубликовано"

### Safety commands
Examples:
- "не публиковать"
- "стоп"
- "только черновик"
- "сначала проверить"

### Approval commands
Examples:
- "одобряю черновик"
- "можно готовить publish gate"
- "не менять цену"
- "не менять количество"

## Hard Rules
- No live eBay action from a casual Telegram message.
- No publish/revise/delete without explicit live gate.
- Always show visual preview before approval.
- Always show protected fields before update.
- Reply in Russian to operator.
- German output only for eBay Germany listing content.
- Voice commands must be transcribed and shown back before risky actions.

## Preview Packet
Each Telegram review packet must show:
- product identity
- source/fallback status
- 8-12 photo gallery/contact sheet
- recommended title
- item specifics
- HTML preview or summary
- critic status
- protected fields
- exact next action

## Approval States
- AWAITING_REVIEW
- REWORK_REQUESTED
- APPROVED_DRAFT_ONLY
- APPROVED_PREPARE_LIVE_GATE
- LIVE_GATE_REQUIRED
- BLOCKED

## Handoffs
- URL_INTAKE_AGENT
- PRODUCT_UNDERSTANDING_AGENT
- PHOTO_AGENT
- TITLE_AGENT
- ITEM_SPECIFICS_AGENT
- HTML_AGENT
- MARKETPLACE_CRITIC_AGENT
- RUNNER_AGENT after gates only

## Stop Conditions
- unclear voice command
- operator asks publish but no critic PASS
- missing visual preview
- protected field mismatch
- server state unknown
- live gate missing

## Next Implementation Layer
Local/Windows sandbox first, then server runtime only after cleanup audit and deploy plan.
