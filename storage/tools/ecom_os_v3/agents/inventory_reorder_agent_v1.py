from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class ReorderDecision:
    sku: str
    decision: str
    reasons: List[str]
    required_checks: List[str]


@dataclass
class InventoryReorderResult:
    status: str
    decisions: List[Dict[str, Any]]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class InventoryReorderAgentV1:
    """Suggests reorder/hold/stop/test-small-batch decisions.

    It never orders products automatically.
    """

    def run(self, products: List[Dict[str, Any]]) -> InventoryReorderResult:
        decisions: List[ReorderDecision] = []
        for item in products:
            sku = str(item.get("sku") or "UNKNOWN_SKU")
            qty = int(item.get("quantity") or 0)
            sales_30d = int(item.get("sales_30d") or item.get("sales") or 0)
            margin_ok = bool(item.get("minimum_margin_ok"))
            supplier_url = item.get("supplier_url")
            stale = bool(item.get("stale_no_movement"))
            reasons: List[str] = []
            checks: List[str] = ["OPERATOR_APPROVAL_BEFORE_ORDER"]

            if stale and sales_30d == 0:
                decision = "DO_NOT_REORDER_REBUILD_OR_REPLACE"
                reasons.append("stale_no_sales")
                checks.append("COMPETITOR_CHECK")
            elif qty <= 3 and sales_30d > 0 and margin_ok and supplier_url:
                decision = "REORDER_CANDIDATE"
                reasons.append("low_stock_sales_present_margin_ok")
                checks += ["SUPPLIER_PRICE_CHECK", "BUDGET_CHECK"]
            elif qty <= 3 and sales_30d > 0 and not margin_ok:
                decision = "HOLD_UNTIL_MARGIN_REVIEW"
                reasons.append("low_stock_but_margin_not_ok")
                checks.append("MARGIN_CHECK")
            elif qty > 10 and sales_30d == 0:
                decision = "HOLD_STOCK_NO_REORDER"
                reasons.append("stock_available_no_recent_sales")
            elif not supplier_url:
                decision = "NEEDS_SUPPLIER_CHECK"
                reasons.append("supplier_url_missing")
            else:
                decision = "MONITOR"
                reasons.append("no_strong_reorder_signal")

            decisions.append(ReorderDecision(sku, decision, reasons, checks))

        return InventoryReorderResult(
            status="PASS",
            decisions=[asdict(x) for x in decisions],
            next_allowed_action="REVIEW_REORDER_DECISIONS_WITH_OPERATOR",
        )
