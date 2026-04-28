"""Verification guard for Brain Hard-Gate dry-run V1.

Dry-run module only. It does not call external APIs, server runtime,
marketplace adapters, or mutate project state.
"""

from __future__ import annotations

from dataclasses import dataclass

from .schemas import ActionRequest, action_looks_live


@dataclass(frozen=True)
class VerificationGuardResult:
    status: str
    allowed_to_advance: bool
    verification_required: bool
    verification_type: str
    reason: str


VERIFICATION_RULES = {
    "publish": "marketplace_visibility_verify",
    "revise": "marketplace_revision_verify",
    "quantity_sync": "inventory_marketplace_consistency_verify",
    "send_offer": "offer_delivery_verify",
    "enable_ads": "ads_status_verify",
    "disable_ads": "ads_status_verify",
    "token_refresh": "token_read_only_verify",
    "server_runtime_restart": "runtime_health_verify",
}


def required_verification_for_action(action: str) -> str:
    normalized = action.lower().strip()
    for token, verify_type in VERIFICATION_RULES.items():
        if token in normalized:
            return verify_type
    if action_looks_live(normalized):
        return "generic_live_action_verify"
    return "none"


def check_verification_requirement(
    request: ActionRequest,
    verification_confirmed: bool = False,
) -> VerificationGuardResult:
    """Return whether a route may advance based on verification state."""
    verification_type = required_verification_for_action(request.requested_action)
    verification_required = request.requires_verification or verification_type != "none"

    if not verification_required:
        return VerificationGuardResult(
            status="ALLOW",
            allowed_to_advance=True,
            verification_required=False,
            verification_type="none",
            reason="verification_not_required",
        )

    if verification_confirmed:
        return VerificationGuardResult(
            status="ALLOW",
            allowed_to_advance=True,
            verification_required=True,
            verification_type=verification_type,
            reason="verification_confirmed",
        )

    return VerificationGuardResult(
        status="CHECK_REQUIRED",
        allowed_to_advance=False,
        verification_required=True,
        verification_type=verification_type,
        reason="verification_required_before_route_advance",
    )
