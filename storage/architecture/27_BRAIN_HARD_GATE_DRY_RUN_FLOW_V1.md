# 27_BRAIN_HARD_GATE_DRY_RUN_FLOW_V1

Status: DRY_RUN_FLOW_DRAFT
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define the first safe execution flow for Brain Hard-Gate before any runtime/live integration.

## Principle
Dry-run must prove that the Brain can ALLOW or BLOCK actions safely without calling eBay, server runtime, Telegram runtime, inventory mutation, or any live adapter.

---

# 1. Dry-run inputs

## 1.1 Pointer input
Brain reads current project state from the known control pointer path:

```text
storage/control_room/CURRENT_POINTER.json
```

Required fields if present:
- current_position
- next_allowed_action
- publish_allowed
- revise_allowed
- delete_allowed
- auto_publish_allowed

If fields are missing, Brain must return CHECK_REQUIRED, not guess.

## 1.2 Action request input
Dry-run action request schema:

```json
{
  "requested_action": "",
  "requested_by": "operator",
  "environment": "GITHUB_AUDIT | LOCAL_WINDOWS | SERVER_RUNTIME | TELEGRAM_INTERFACE",
  "target_module": "",
  "risk_level": "read_only | draft | live | dangerous",
  "approval_reference": null,
  "requires_verification": true
}
```

---

# 2. Dry-run test cases

## CASE A — Safe read-only action
Input:
```json
{
  "requested_action": "verify_pointer_state_v1",
  "requested_by": "operator",
  "environment": "LOCAL_WINDOWS",
  "target_module": "brain_orchestrator",
  "risk_level": "read_only",
  "approval_reference": null,
  "requires_verification": false
}
```

Expected:
- ALLOW if route permits or CHECK_REQUIRED if next_allowed_action is different.
- No live calls.
- Audit written.

## CASE B — Publish without approval
Input:
```json
{
  "requested_action": "publish_offer_v1",
  "requested_by": "telegram",
  "environment": "TELEGRAM_INTERFACE",
  "target_module": "ebay_adapter",
  "risk_level": "live",
  "approval_reference": null,
  "requires_verification": true
}
```

Expected:
- BLOCK.
- Reason: publish requires approval and Telegram cannot publish directly.
- No live calls.
- Russian operator message created.

## CASE C — Wrong environment
Input:
```json
{
  "requested_action": "server_runtime_restart_v1",
  "requested_by": "operator",
  "environment": "GITHUB_AUDIT",
  "target_module": "server_runtime",
  "risk_level": "dangerous",
  "approval_reference": null,
  "requires_verification": true
}
```

Expected:
- BLOCK.
- Reason: GitHub audit branch cannot execute server runtime action.
- No server call.

## CASE D — Valid approved live action simulation
Input:
```json
{
  "requested_action": "publish_offer_v1",
  "requested_by": "operator",
  "environment": "SERVER_RUNTIME",
  "target_module": "ebay_adapter",
  "risk_level": "live",
  "approval_reference": "approved_test_reference_only",
  "requires_verification": true
}
```

Expected:
- CHECK_REQUIRED or ALLOW_DRY_RUN_ONLY.
- Never call live publish during dry-run.
- Confirm verification would be required after live action.

---

# 3. Decision logic

Brain dry-run decision order:

```text
1. Load pointer
2. Validate pointer readable
3. Load action request
4. Check environment permission
5. Check forbidden direct path
6. Check next_allowed_action compatibility
7. Check approval requirement
8. Check verification requirement
9. Return ALLOW / BLOCK / CHECK_REQUIRED / ALLOW_DRY_RUN_ONLY
10. Write audit event
11. Generate Russian operator message
```

---

# 4. Audit output

Target draft output:

```text
storage/state_control/brain_hard_gate_dry_run_decision_v1.json
```

Schema:

```json
{
  "status": "ALLOW | BLOCK | CHECK_REQUIRED | ALLOW_DRY_RUN_ONLY",
  "layer": "BRAIN_HARD_GATE_DRY_RUN_V1",
  "requested_action": "",
  "next_allowed_action": "",
  "environment": "",
  "target_module": "",
  "risk_level": "",
  "approval_required": false,
  "approval_present": false,
  "verification_required": false,
  "forbidden_path_detected": false,
  "decision_reason": "",
  "live_called": false,
  "server_touched": false,
  "publish_called": false,
  "timestamp": ""
}
```

---

# 5. Russian operator messages

Examples:

## Allowed read-only
```text
Разрешено: read-only проверка безопасна. Live-действия не запускались.
```

## Blocked publish
```text
Блокировано: publish требует approval gate и не может запускаться напрямую из Telegram. Live publish не запускался.
```

## Wrong environment
```text
Блокировано: это действие относится к server runtime, но запрошено из GitHub audit. Сервер не тронут.
```

## Verification required
```text
Проверка обязательна: API-успех не считается финальным результатом без marketplace visibility verify.
```

---

# 6. Success criteria

Dry-run flow is successful when:
- safe read-only request is handled without live call;
- publish without approval is blocked;
- wrong environment is blocked;
- approved live simulation never calls live adapter;
- audit output records all decisions;
- Russian operator message is generated.

---

# 7. Stop conditions

Stop if:
- pointer path is unclear;
- approval model is unclear;
- dry-run tries to call live adapter;
- server runtime would be touched;
- audit output cannot be written safely;
- action risk cannot be classified.

STOP: This document defines dry-run flow only. It does not implement or execute runtime code.
