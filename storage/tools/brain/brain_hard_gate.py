"""Unified Brain Hard-Gate orchestrator for dry-run V1.

This module composes pointer loading, action validation, environment guard,
approval guard, forbidden path guard, verification guard, audit writing,
and Russian operator messages.

Dry-run safety:
- no live marketplace calls
- no server runtime calls
- no secret reads
- no inventory mutation
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .action_request_loader import load_action_request_from_dict
from .approval_guard import check_approval
from .audit_writer import BrainDecisionAudit, write_decision_audit
from .environment_guard import check_environment
from .forbidden_path_guard import check_forbidden_path
from .operator_message_ru import message_for_status
from .pointer_loader import load_pointer
from .schemas import ActionRequest
from .verification_guard import check_verification_requirement


@dataclass(frozen=True)
class BrainGateDecision:
    status: str
    reason: str
    operator_message_ru: str
    audit_path: str
    live_called: bool = False
    server_touched: bool = False
    publish_called: bool = False


def _finalize_decision(
    *,
    root: Path,
    status: str,
    reason: str,
    request: ActionRequest | None,
    next_allowed_action: str = "",
    approval_required: bool = False,
    approval_present: bool = False,
    approval_valid: bool = False,
    verification_required: bool = False,
    forbidden_path_detected: bool = False,
) -> BrainGateDecision:
    message = message_for_status(status, reason)

    audit = BrainDecisionAudit(
        status=status,
        layer="BRAIN_HARD_GATE_DRY_RUN_V1",
        requested_action=request.requested_action if request else "",
        next_allowed_action=next_allowed_action,
        environment=request.environment if request else "",
        target_module=request.target_module if request else "",
        risk_level=request.risk_level if request else "",
        approval_required=approval_required,
        approval_present=approval_present,
        approval_valid=approval_valid,
        verification_required=verification_required,
        forbidden_path_detected=forbidden_path_detected,
        decision_reason=reason,
        operator_message_ru=message.message_ru,
        live_called=False,
        server_touched=False,
        publish_called=False,
    )
    audit_path = write_decision_audit(audit, root=root)
    return BrainGateDecision(
        status=status,
        reason=reason,
        operator_message_ru=message.message_ru,
        audit_path=str(audit_path),
        live_called=False,
        server_touched=False,
        publish_called=False,
    )


def evaluate_action(
    action_data: dict[str, Any],
    *,
    root: Path | None = None,
    approval_data: dict[str, Any] | None = None,
    verification_confirmed: bool = False,
    dry_run: bool = True,
) -> BrainGateDecision:
    """Evaluate an action request through Brain Hard-Gate.

    This function is deterministic for the same pointer, action_data,
    approval_data, and verification_confirmed values.
    """
    project_root = root or Path.cwd()

    pointer_result = load_pointer(root=project_root)
    if pointer_result.status != "OK":
        return _finalize_decision(
            root=project_root,
            status=pointer_result.status,
            reason=",".join(pointer_result.errors) or "pointer_not_ok",
            request=None,
            next_allowed_action=pointer_result.next_allowed_action,
        )

    request_result = load_action_request_from_dict(action_data)
    request = request_result.request
    if request_result.status != "OK" or request is None:
        return _finalize_decision(
            root=project_root,
            status="BLOCK",
            reason=",".join(request_result.errors) or "action_request_invalid",
            request=request,
            next_allowed_action=pointer_result.next_allowed_action,
        )

    env_result = check_environment(request)
    if not env_result.allowed:
        return _finalize_decision(
            root=project_root,
            status="BLOCK",
            reason=env_result.reason,
            request=request,
            next_allowed_action=pointer_result.next_allowed_action,
        )

    forbidden_result = check_forbidden_path(request)
    if not forbidden_result.allowed:
        return _finalize_decision(
            root=project_root,
            status="BLOCK",
            reason=forbidden_result.reason,
            request=request,
            next_allowed_action=pointer_result.next_allowed_action,
            forbidden_path_detected=True,
        )

    if request.requested_action != pointer_result.next_allowed_action:
        return _finalize_decision(
            root=project_root,
            status="CHECK_REQUIRED",
            reason="requested_action_does_not_match_next_allowed_action",
            request=request,
            next_allowed_action=pointer_result.next_allowed_action,
        )

    approval_result = check_approval(request, approval_data=approval_data)
    if not approval_result.allowed:
        return _finalize_decision(
            root=project_root,
            status="BLOCK",
            reason=approval_result.reason,
            request=request,
            next_allowed_action=pointer_result.next_allowed_action,
            approval_required=approval_result.approval_required,
            approval_present=approval_result.approval_present,
            approval_valid=approval_result.approval_valid,
        )

    verification_result = check_verification_requirement(
        request,
        verification_confirmed=verification_confirmed,
    )

    if verification_result.verification_required and dry_run:
        return _finalize_decision(
            root=project_root,
            status="ALLOW_DRY_RUN_ONLY",
            reason=verification_result.reason,
            request=request,
            next_allowed_action=pointer_result.next_allowed_action,
            approval_required=approval_result.approval_required,
            approval_present=approval_result.approval_present,
            approval_valid=approval_result.approval_valid,
            verification_required=True,
        )

    if not verification_result.allowed_to_advance:
        return _finalize_decision(
            root=project_root,
            status="CHECK_REQUIRED",
            reason=verification_result.reason,
            request=request,
            next_allowed_action=pointer_result.next_allowed_action,
            approval_required=approval_result.approval_required,
            approval_present=approval_result.approval_present,
            approval_valid=approval_result.approval_valid,
            verification_required=True,
        )

    return _finalize_decision(
        root=project_root,
        status="ALLOW",
        reason="all_brain_hard_gate_checks_passed",
        request=request,
        next_allowed_action=pointer_result.next_allowed_action,
        approval_required=approval_result.approval_required,
        approval_present=approval_result.approval_present,
        approval_valid=approval_result.approval_valid,
        verification_required=verification_result.verification_required,
    )
