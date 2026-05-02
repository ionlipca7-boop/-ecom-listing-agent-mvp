from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class MarketplaceAccessGateResult:
    status: str
    marketplace: str
    checks: Dict[str, str]
    blocked_reasons: List[str]
    required_before_live: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MarketplaceAccessGateAgentV1:
    """Universal marketplace preflight gate.

    This agent decides whether a marketplace route is open before any publish,
    revise, offer, price, photo, or delete action. It does not call marketplace
    APIs by itself; it reads preflight results from marketplace-specific guards.
    """

    def run(self, marketplace: str, preflight: Dict[str, Any], live_scope: Dict[str, Any] | None = None) -> MarketplaceAccessGateResult:
        marketplace = (marketplace or "unknown").lower()
        live_scope = live_scope or {}
        checks: Dict[str, str] = {}
        blocked: List[str] = []

        checks["marketplace_supported"] = "PASS" if marketplace in {"ebay_de", "ebay", "ebay_de_production"} else "BLOCKED"
        if checks["marketplace_supported"] != "PASS":
            blocked.append("marketplace_not_supported_in_v1")

        checks["token_preflight"] = str(preflight.get("status") or "MISSING")
        if not str(preflight.get("status") or "").startswith("PASS"):
            blocked.append("token_preflight_not_pass")

        checks["env_present"] = "PASS" if preflight.get("env_present") else "BLOCKED"
        if checks["env_present"] != "PASS":
            blocked.append("required_env_missing")

        checks["secret_leak_scan"] = str(preflight.get("secret_scan_status") or "NOT_RUN")
        if checks["secret_leak_scan"] == "BLOCKED":
            blocked.append("secret_leak_scan_blocked")

        checks["live_scope_defined"] = "PASS" if live_scope.get("scope_id") and live_scope.get("allowed_action") else "BLOCKED"
        if checks["live_scope_defined"] != "PASS":
            blocked.append("live_scope_missing")

        checks["operator_approval"] = "PASS" if live_scope.get("operator_approval") is True else "BLOCKED"
        if checks["operator_approval"] != "PASS":
            blocked.append("operator_approval_missing")

        checks["protected_fields_reviewed"] = "PASS" if live_scope.get("protected_fields_reviewed") is True else "BLOCKED"
        if checks["protected_fields_reviewed"] != "PASS":
            blocked.append("protected_fields_not_reviewed")

        required = [
            "valid_or_refreshed_marketplace_token",
            "secret_scan_PASS",
            "readonly_before_state",
            "exact_payload_review",
            "operator_approval",
            "protected_fields_review",
            "runtime_owner_check",
            "readonly_after_state_after_action",
        ]

        status = "PASS_MARKETPLACE_ACCESS_OPEN" if not blocked else "BLOCKED_MARKETPLACE_ACCESS_CLOSED"
        return MarketplaceAccessGateResult(
            status=status,
            marketplace=marketplace,
            checks=checks,
            blocked_reasons=blocked,
            required_before_live=required,
            next_allowed_action="LIVE_GATE_PAYLOAD_REVIEW" if status.startswith("PASS") else "FIX_ACCESS_GATE_BLOCKERS",
        )
