"""Forbidden path guard for Brain Hard-Gate dry-run V1.

Policy:
- Explicitly block known unsafe direct execution paths.
- Deny by default for unclear high-risk routes.
- No live calls and no runtime mutation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .schemas import ActionRequest, action_looks_live


@dataclass(frozen=True)
class ForbiddenPathResult:
    status: str
    allowed: bool
    forbidden_path_detected: bool
    reason: str


FORBIDDEN_ROUTE_PATTERNS = (
    ("TELEGRAM_INTERFACE", "ebay", "telegram_to_ebay_direct"),
    ("TELEGRAM_INTERFACE", "marketplace_live", "telegram_to_marketplace_live_direct"),
    ("TELEGRAM_INTERFACE", "inventory_live_mutation", "telegram_to_inventory_live_direct"),
    ("GITHUB_AUDIT", "server_runtime", "github_audit_to_server_runtime"),
    ("GITHUB_AUDIT", "ebay_adapter_live", "github_audit_to_ebay_live"),
    ("GITHUB_AUDIT", "marketplace_live", "github_audit_to_marketplace_live"),
    ("LOCAL_WINDOWS", "server_runtime_live", "local_to_server_runtime_live_without_gate"),
    ("LOCAL_WINDOWS", "ebay_adapter_live", "local_to_ebay_live_without_gate"),
)

FORBIDDEN_TARGET_TOKENS = {
    "secrets",
    "print_token",
    "dump_env",
    "direct_publish",
    "direct_delete",
    "direct_revise",
    "bypass_brain",
    "bypass_approval",
    "bypass_verify",
}


def check_forbidden_path(request: ActionRequest) -> ForbiddenPathResult:
    """Detect direct routes that must never be allowed."""
    environment = request.environment
    target_module = request.target_module.lower().strip()
    requested_action = request.requested_action.lower().strip()

    combined = f"{target_module}:{requested_action}"

    for env, token, reason in FORBIDDEN_ROUTE_PATTERNS:
        if environment == env and token in combined:
            return ForbiddenPathResult(
                status="BLOCK",
                allowed=False,
                forbidden_path_detected=True,
                reason=reason,
            )

    for token in FORBIDDEN_TARGET_TOKENS:
        if token in combined:
            return ForbiddenPathResult(
                status="BLOCK",
                allowed=False,
                forbidden_path_detected=True,
                reason=f"forbidden_token_detected:{token}",
            )

    if request.requested_by.lower().strip() in {"agent", "tool"} and action_looks_live(requested_action):
        return ForbiddenPathResult(
            status="BLOCK",
            allowed=False,
            forbidden_path_detected=True,
            reason="agent_or_tool_live_action_requires_brain_and_approval",
        )

    return ForbiddenPathResult(
        status="ALLOW",
        allowed=True,
        forbidden_path_detected=False,
        reason="no_forbidden_path_detected",
    )
