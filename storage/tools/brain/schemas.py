"""Schemas and constants for Brain Hard-Gate dry-run V1.

Safety policy:
- No live calls.
- No server runtime calls.
- No secret access.
- No marketplace publish/revise/delete.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

Environment = Literal[
    "LOCAL_WINDOWS",
    "GITHUB_AUDIT",
    "SERVER_RUNTIME",
    "TELEGRAM_INTERFACE",
]

RiskLevel = Literal[
    "read_only",
    "draft",
    "live",
    "dangerous",
]

DecisionStatus = Literal[
    "ALLOW",
    "BLOCK",
    "CHECK_REQUIRED",
    "ALLOW_DRY_RUN_ONLY",
]

VALID_ENVIRONMENTS = {
    "LOCAL_WINDOWS",
    "GITHUB_AUDIT",
    "SERVER_RUNTIME",
    "TELEGRAM_INTERFACE",
}

VALID_RISK_LEVELS = {
    "read_only",
    "draft",
    "live",
    "dangerous",
}

DECISION_STATUSES = {
    "ALLOW",
    "BLOCK",
    "CHECK_REQUIRED",
    "ALLOW_DRY_RUN_ONLY",
}

APPROVAL_REQUIRED_RISK_LEVELS = {
    "live",
    "dangerous",
}

LIVE_ACTION_KEYWORDS = {
    "publish",
    "revise",
    "delete",
    "send_offer",
    "enable_ads",
    "disable_ads",
    "quantity_sync",
    "server_runtime_restart",
}

SAFETY_DEFAULTS = {
    "live_called": False,
    "server_touched": False,
    "publish_called": False,
}


@dataclass(frozen=True)
class ActionRequest:
    requested_action: str
    requested_by: str
    environment: str
    target_module: str
    risk_level: str
    approval_reference: str | None = None
    requires_verification: bool = True
    timestamp: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ActionRequest":
        return cls(
            requested_action=str(data.get("requested_action", "")).strip(),
            requested_by=str(data.get("requested_by", "operator")).strip(),
            environment=str(data.get("environment", "")).strip(),
            target_module=str(data.get("target_module", "")).strip(),
            risk_level=str(data.get("risk_level", "")).strip(),
            approval_reference=data.get("approval_reference"),
            requires_verification=bool(data.get("requires_verification", True)),
            timestamp=str(data.get("timestamp", "")).strip(),
        )


def validate_action_request(request: ActionRequest) -> list[str]:
    """Return a list of validation errors. Empty list means schema-level valid."""
    errors: list[str] = []
    if not request.requested_action:
        errors.append("missing_requested_action")
    if request.environment not in VALID_ENVIRONMENTS:
        errors.append("unknown_environment")
    if request.risk_level not in VALID_RISK_LEVELS:
        errors.append("unknown_risk_level")
    if not request.target_module:
        errors.append("missing_target_module")
    return errors


def action_looks_live(action: str) -> bool:
    normalized = action.lower().strip()
    return any(keyword in normalized for keyword in LIVE_ACTION_KEYWORDS)
