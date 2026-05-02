from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class PriceCompetitionResult:
    status: str
    sku: str
    recommended_action: str
    price_position: str
    issues: List[str]
    notes: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PriceCompetitionAgentV1:
    """Local deterministic price/competition evaluator.

    It does not browse marketplaces. It uses provided competitor snapshots only.
    For real pricing decisions, fresh web/marketplace data is required later.
    """

    def run(self, product: Dict[str, Any]) -> PriceCompetitionResult:
        sku = str(product.get("sku") or product.get("product_identity") or "UNKNOWN_SKU")
        price = float(product.get("price") or 0)
        min_safe = product.get("minimum_safe_price")
        competitors = list(product.get("competitors") or [])
        margin_known = bool(product.get("margin_known"))
        issues: List[str] = []
        notes: List[str] = []

        if price <= 0:
            issues.append("own_price_missing")
        if not margin_known:
            issues.append("margin_unknown")
        if not competitors:
            notes.append("competitor_snapshot_missing_use_fresh_web_later")
            position = "UNKNOWN_NO_COMPETITOR_DATA"
            action = "GET_COMPETITOR_SNAPSHOT_BEFORE_PRICE_CHANGE"
        else:
            comp_prices = [float(c.get("price")) for c in competitors if c.get("price") is not None]
            if not comp_prices:
                position = "UNKNOWN_COMPETITOR_PRICE_MISSING"
                action = "FIX_COMPETITOR_SNAPSHOT"
            else:
                avg = sum(comp_prices) / len(comp_prices)
                if price > avg * 1.15:
                    position = "ABOVE_MARKET"
                    action = "PRICE_OR_VALUE_REVIEW_CANDIDATE"
                elif price < avg * 0.85:
                    position = "BELOW_MARKET"
                    action = "MARGIN_AND_PRICE_INCREASE_REVIEW"
                else:
                    position = "WITHIN_MARKET_RANGE"
                    action = "KEEP_PRICE_OR_TEST_VISUAL_REFRESH"
                notes.append(f"competitor_average={avg:.2f}")

        if min_safe is not None and price < float(min_safe):
            issues.append("price_below_minimum_safe_price")

        status = "PASS" if "own_price_missing" not in issues else "BLOCKED"
        return PriceCompetitionResult(
            status=status,
            sku=sku,
            recommended_action=action,
            price_position=position,
            issues=issues,
            notes=notes,
            next_allowed_action="REVIEW_PRICE_DECISION_WITH_OPERATOR" if status == "PASS" else "FIX_PRICE_INPUT",
        )
