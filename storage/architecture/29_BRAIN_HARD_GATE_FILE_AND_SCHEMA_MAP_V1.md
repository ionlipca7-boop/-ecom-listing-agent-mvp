# 29_BRAIN_HARD_GATE_FILE_AND_SCHEMA_MAP_V1

Status: FILE_SCHEMA_MAP_DRAFT
Branch: architecture-audit-v1
Main changed: false
Server touched: false
Live actions called: false

## Purpose
Define exact files and JSON schemas needed for the first Brain Hard-Gate dry-run implementation.

## Core principle
Schemas must be explicit before code is written. Brain Hard-Gate must not guess current state, approval, environment, or verification status.

---

# 1. Input files

## 1.1 Current pointer
Path:
```text
storage/control_room/CURRENT_POINTER.json
```

Expected schema:
```json
{
  "status": "OK | CHECK_REQUIRED | BLOCKED",
  "current_position": "",
  "next_allowed_action": "",
  "last_confirmed_layer": "",
  "publish_allowed": false,
  "revise_allowed": false,
  "delete_allowed": false,
  "auto_publish_allowed": false,
  "updated_at": ""
}
```

Required for first dry-run:
- current_position
- next_allowed_action

Optional but recommended:
- publish_allowed
- revise_allowed
- delete_allowed
- auto_publish_allowed

Failure behavior:
- Missing file -> CHECK_REQUIRED
- Invalid JSON -> BLOCK
- Missing next_allowed_action -> CHECK_REQUIRED

---

## 1.2 Action request
Future path for dry-run input:
```text
storage/state_control/brain_hard_gate_action_request_v1.json
```

Schema:
```json
{
  "requested_action": "",
  "requested_by": "operator | telegram | system | tool",
  "environment": "LOCAL_WINDOWS | GITHUB_AUDIT | SERVER_RUNTIME | TELEGRAM_INTERFACE",
  "target_module": "",
  "risk_level": "read_only | draft | live | dangerous",
  "approval_reference": null,
  "requires_verification": true,
  "timestamp": ""
}
```

Failure behavior:
- Missing action -> BLOCK
- Unknown environment -> BLOCK
- Unknown risk level -> BLOCK
- Live/dangerous action without approval -> BLOCK

---

## 1.3 Approval state
Future path:
```text
storage/state_control/approval_gate_state_v1.json
```

Schema:
```json
{
  "status": "APPROVED | PENDING | DENIED | NOT_REQUIRED",
  "approved_action": "",
  "approval_scope": "read_only | draft | one_live_action | dangerous_action",
  "approved_by": "operator",
  "approval_source": "telegram | chat | file",
  "expires_at": "",
  "single_use": true,
  "used": false
}
```

Rules:
- Approval action must match requested_action.
- Expired approval is invalid.
- Used single-use approval is invalid.
- Approval for one live action cannot authorize batch actions.

---

## 1.4 Environment rules
Future path:
```text
storage/rules/environment_action_matrix_v1.json
```

Schema:
```json
{
  "GITHUB_AUDIT": {
    "allowed_risk_levels": ["read_only", "draft"],
    "forbidden_modules": ["server_runtime", "ebay_adapter_live", "inventory_live_mutation"]
  },
  "LOCAL_WINDOWS": {
    "allowed_risk_levels": ["read_only", "draft"],
    "forbidden_modules": ["server_runtime_live", "ebay_adapter_live"]
  },
  "SERVER_RUNTIME": {
    "allowed_risk_levels": ["read_only", "draft", "live", "dangerous"],
    "requires_approval_for": ["live", "dangerous"]
  },
  "TELEGRAM_INTERFACE": {
    "allowed_risk_levels": ["read_only", "draft"],
    "forbidden_modules": ["ebay_adapter_live", "inventory_live_mutation"]
  }
}
```

---

# 2. Output files

## 2.1 Brain decision audit
Path:
```text
storage/state_control/brain_hard_gate_decision_v1.json
```

Schema:
```json
{
  "status": "ALLOW | BLOCK | CHECK_REQUIRED | ALLOW_DRY_RUN_ONLY",
  "layer": "BRAIN_HARD_GATE_V1",
  "requested_action": "",
  "next_allowed_action": "",
  "environment": "",
  "target_module": "",
  "risk_level": "",
  "approval_required": false,
  "approval_present": false,
  "approval_valid": false,
  "verification_required": false,
  "forbidden_path_detected": false,
  "decision_reason": "",
  "operator_message_ru": "",
  "live_called": false,
  "server_touched": false,
  "publish_called": false,
  "timestamp": ""
}
```

Required safety fields:
- live_called
- server_touched
- publish_called

These must default to false in dry-run.

---

## 2.2 Dry-run result
Path:
```text
storage/state_control/brain_hard_gate_dry_run_result_v1.json
```

Schema:
```json
{
  "status": "PASS | FAIL | CHECK_REQUIRED",
  "test_cases": [
    {
      "name": "",
      "expected": "",
      "actual": "",
      "passed": false,
      "reason": ""
    }
  ],
  "summary": {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "live_called": false,
    "server_touched": false,
    "publish_called": false
  },
  "timestamp": ""
}
```

---

# 3. Runtime module files

Future implementation root:
```text
storage/tools/brain/
```

Suggested files:

```text
__init__.py
schemas.py
pointer_loader.py
action_request_loader.py
approval_guard.py
environment_guard.py
forbidden_path_guard.py
verification_guard.py
audit_writer.py
operator_message_ru.py
dry_run_validator.py
brain_hard_gate.py
```

## File responsibilities

### schemas.py
Owns JSON schema constants and validation helpers.

### pointer_loader.py
Reads CURRENT_POINTER.json safely.

### action_request_loader.py
Reads or constructs action request.

### approval_guard.py
Checks approval validity.

### environment_guard.py
Checks environment/action compatibility.

### forbidden_path_guard.py
Detects forbidden direct paths.

### verification_guard.py
Determines whether verification is required before route advancement.

### audit_writer.py
Writes decision audit JSON.

### operator_message_ru.py
Creates short Russian operator messages.

### dry_run_validator.py
Runs safe dry-run test cases.

### brain_hard_gate.py
Orchestrates all guards and returns decision.

---

# 4. Validation rules

Brain decision must be deterministic:
- same pointer + same request + same approval state = same decision.

Brain must fail closed:
- unknown state -> BLOCK or CHECK_REQUIRED.
- never allow live action by default.

Brain must write audit before returning final result.

---

# 5. First implementation success condition

Implementation is ready to begin when:
- this schema map is accepted;
- no schema conflicts remain;
- dry-run result schema exists;
- decision audit schema exists;
- action request schema exists;
- safety defaults are false.

STOP: This file defines schemas only. It does not implement runtime code.
