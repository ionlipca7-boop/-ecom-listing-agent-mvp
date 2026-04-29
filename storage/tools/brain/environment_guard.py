"""Environment guard for Brain Hard-Gate dry-run V1.

Policy:
- Deny by default.
- Fail closed on unknown environment/risk/module.
- No live calls and no runtime mutation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .schemas import ActionRequest, VALID_ENVIRONMENTS, VALID_RISK_LEVELS


@dataclass(frozen=True)
class GuardResult:
    status: str
    allowed: bool
    reason: str


ENVIRONMENT_RULES = {
    "GITHUB_AUDIT": {
        "allowed_risk_levels": {"read_only", "draft"},
        "forbidden_module_tokens": {
            "server_runtime",
            "ebay_adapter_live",
            "inventory_live_mutation",
            "marketplace_live",
            "secrets",
        },
    },
    "LOCAL_WINDOWS": {
        "allowed_risk_levels": {"read_only", "draft"},
        "forbidden_module_tokens": {
            "server_runtime_live",
            "ebay_adapter_live",
            "marketplace_live",
            "secrets",
        },
    },
    "SERVER_RUNTIME": {
        "allowed_risk_levels": {"read_only", "draft", "live", "dangerous"},
        "forbidden_module_tokens": set(),
    },
    "TELEGRAM_INTERFACE": {
        "allowed_risk_levels": {"read_only", "draft"},
        "forbidden_module_tokens": {
            "ebay_adapter_live",
            "inventory_live_mutation",
            "marketplace_live",
            "server_runtime",
            "secrets",
        },
    },
}


def check_environment(request: ActionRequest) -> GuardResult:
    """Validate that the request is allowed in its declared environment."""
    environment = request.environment
    risk_level = request.risk_level
    target_module = request.target_module.lower().strip()

    if environment not in VALID_ENVIRONMENTS:
        return GuardResult(
            status="BLOCK",
            allowed=False,
            reason="unknown_environment",
        )

    if risk_level not in VALID_RISK_LEVELS:
        return GuardResult(
            status="BLOCK",
            allowed=False,
            reason="unknown_risk_level",
        )

    rules = ENVIRONMENT_RULES.get(environment)
    if not rules:
        return GuardResult(
            status="BLOCK",
            allowed=False,
            reason="environment_rules_missing",
        )

    allowed_risk_levels = rules["allowed_risk_levels"]
    if risk_level not in allowed_risk_levels:
        return GuardResult(
            status="BLOCK",
            allowed=False,
            reason=f"risk_level_not_allowed_in_environment:{risk_level}:{environment}",
        )

    for token in rules["forbidden_module_tokens"]:
        if token in target_module:
            return GuardResult(
                status="BLOCK",
                allowed=False,
                reason=f"target_module_forbidden_in_environment:{token}:{environment}",
            )

    return GuardResult(
        status="ALLOW",
        allowed=True,
        reason="environment_allowed",
    )
