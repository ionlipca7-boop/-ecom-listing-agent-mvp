"""Approval guard for Brain Hard-Gate dry-run V1.

Policy:
- Live and dangerous actions require explicit matching approval.
- Approval must match requested_action.
- Single-use approvals cannot be reused.
- Missing/invalid approval fails closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .schemas import APPROVAL_REQUIRED_RISK_LEVELS, ActionRequest, action_looks_live


@dataclass(frozen=True)
class ApprovalState:
    status: str
    approved_action: str
    approval_scope: str
    approved_by: str
    approval_source: str
    expires_at: str
    single_use: bool
    used: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "ApprovalState | None":
        if not isinstance(data, dict):
            return None
        return cls(
            status=str(data.get("status", "")).strip(),
            approved_action=str(data.get("approved_action", "")).strip(),
            approval_scope=str(data.get("approval_scope", "")).strip(),
            approved_by=str(data.get("approved_by", "")).strip(),
            approval_source=str(data.get("approval_source", "")).strip(),
            expires_at=str(data.get("expires_at", "")).strip(),
            single_use=bool(data.get("single_use", True)),
            used=bool(data.get("used", False)),
        )


@dataclass(frozen=True)
class ApprovalGuardResult:
    status: str
    allowed: bool
    approval_required: bool
    approval_present: bool
    approval_valid: bool
    reason: str


def _is_expired(expires_at: str) -> bool:
    if not expires_at:
        return False
    try:
        normalized = expires_at.replace("Z", "+00:00")
        expiry = datetime.fromisoformat(normalized)
    except ValueError:
        return True
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) > expiry.astimezone(timezone.utc)


def approval_required_for(request: ActionRequest) -> bool:
    if request.risk_level in APPROVAL_REQUIRED_RISK_LEVELS:
        return True
    return action_looks_live(request.requested_action)


def check_approval(request: ActionRequest, approval_data: dict[str, Any] | None = None) -> ApprovalGuardResult:
    """Validate approval for an action request."""
    approval_required = approval_required_for(request)
    approval_state = ApprovalState.from_dict(approval_data)

    if not approval_required:
        return ApprovalGuardResult(
            status="ALLOW",
            allowed=True,
            approval_required=False,
            approval_present=approval_state is not None,
            approval_valid=True,
            reason="approval_not_required",
        )

    if approval_state is None:
        return ApprovalGuardResult(
            status="BLOCK",
            allowed=False,
            approval_required=True,
            approval_present=False,
            approval_valid=False,
            reason="approval_missing",
        )

    if approval_state.status != "APPROVED":
        return ApprovalGuardResult(
            status="BLOCK",
            allowed=False,
            approval_required=True,
            approval_present=True,
            approval_valid=False,
            reason=f"approval_status_not_approved:{approval_state.status}",
        )

    if approval_state.approved_action != request.requested_action:
        return ApprovalGuardResult(
            status="BLOCK",
            allowed=False,
            approval_required=True,
            approval_present=True,
            approval_valid=False,
            reason="approval_action_mismatch",
        )

    if approval_state.single_use and approval_state.used:
        return ApprovalGuardResult(
            status="BLOCK",
            allowed=False,
            approval_required=True,
            approval_present=True,
            approval_valid=False,
            reason="approval_already_used",
        )

    if _is_expired(approval_state.expires_at):
        return ApprovalGuardResult(
            status="BLOCK",
            allowed=False,
            approval_required=True,
            approval_present=True,
            approval_valid=False,
            reason="approval_expired_or_invalid_expiry",
        )

    return ApprovalGuardResult(
        status="ALLOW",
        allowed=True,
        approval_required=True,
        approval_present=True,
        approval_valid=True,
        reason="approval_valid",
    )
