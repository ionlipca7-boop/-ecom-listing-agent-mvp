"""Audit writer for Brain Hard-Gate dry-run V1.

Security policy:
- Do not write secrets/tokens/env values.
- Sanitize strings to reduce log-injection risk.
- Ensure dry-run safety flags exist and default to False.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_DECISION_AUDIT_PATH = Path("storage/state_control/brain_hard_gate_decision_v1.json")

SENSITIVE_KEYS = {
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "client_secret",
    "password",
    "authorization",
    "api_key",
}


@dataclass(frozen=True)
class BrainDecisionAudit:
    status: str
    layer: str
    requested_action: str
    next_allowed_action: str
    environment: str
    target_module: str
    risk_level: str
    approval_required: bool
    approval_present: bool
    approval_valid: bool
    verification_required: bool
    forbidden_path_detected: bool
    decision_reason: str
    operator_message_ru: str
    live_called: bool = False
    server_touched: bool = False
    publish_called: bool = False
    timestamp: str = ""

    def to_safe_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = data.get("timestamp") or datetime.now(timezone.utc).isoformat()
        data["live_called"] = bool(data.get("live_called", False))
        data["server_touched"] = bool(data.get("server_touched", False))
        data["publish_called"] = bool(data.get("publish_called", False))
        return sanitize_for_audit(data)


def sanitize_for_audit(value: Any) -> Any:
    """Sanitize audit value recursively.

    This avoids accidental secret logging and strips CR/LF from strings to reduce
    log injection risks.
    """
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            key_str = str(key)
            if key_str.lower() in SENSITIVE_KEYS or any(s in key_str.lower() for s in SENSITIVE_KEYS):
                cleaned[key_str] = "[REDACTED]"
            else:
                cleaned[key_str] = sanitize_for_audit(item)
        return cleaned
    if isinstance(value, list):
        return [sanitize_for_audit(item) for item in value]
    if isinstance(value, str):
        return value.replace("\r", " ").replace("\n", " ").strip()
    return value


def write_decision_audit(
    audit: BrainDecisionAudit,
    root: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    """Write Brain decision audit JSON.

    This function creates parent directories if needed and writes UTF-8 JSON.
    It does not perform any live action.
    """
    project_root = root or Path.cwd()
    relative_output_path = output_path or DEFAULT_DECISION_AUDIT_PATH
    full_path = project_root / relative_output_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(
        json.dumps(audit.to_safe_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return full_path
