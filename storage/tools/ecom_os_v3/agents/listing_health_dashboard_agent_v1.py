from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class HealthRow:
    sku: str
    listing_id: str
    days_live: int
    price: float
    quantity: int
    views: int
    watchers: int
    sales: int
    ad_rate: float
    health_state: str
    priority: str
    next_action: str


@dataclass
class ListingHealthDashboardResult:
    status: str
    rows: List[Dict[str, Any]]
    summary: Dict[str, int]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ListingHealthDashboardAgentV1:
    """Creates a portfolio health dashboard for 50-100 listings.

    It recommends only. It never changes listings.
    """

    def run(self, listings: List[Dict[str, Any]]) -> ListingHealthDashboardResult:
        rows: List[HealthRow] = []
        summary: Dict[str, int] = {}

        for item in listings:
            sku = str(item.get("sku") or "UNKNOWN_SKU")
            listing_id = str(item.get("listing_id") or "UNKNOWN_LISTING")
            days = int(item.get("days_live") or 0)
            price = float(item.get("price") or 0)
            qty = int(item.get("quantity") or 0)
            views = int(item.get("views") or 0)
            watchers = int(item.get("watchers") or 0)
            sales = int(item.get("sales") or 0)
            ad_rate = float(item.get("ad_rate") or 0)
            impressions = int(item.get("impressions") or 0)

            if qty <= 0:
                state, priority, action = "OUT_OF_STOCK", "P1_REVENUE_RISK", "RESTOCK_OR_PAUSE_REVIEW"
            elif sales > 0:
                state, priority, action = "HEALTHY_SELLING", "P4_NO_ACTION", "KEEP_MONITORING"
            elif days < 3:
                state, priority, action = "NEW_UNDER_OBSERVATION", "P3_MONITOR", "WAIT"
            elif impressions < 50:
                state, priority, action = "IMPRESSIONS_LOW", "P2_REFRESH_NEEDED", "TITLE_KEYWORD_REVIEW"
            elif views < 10 and days >= 5:
                state, priority, action = "VIEWS_LOW", "P2_REFRESH_NEEDED", "MAIN_PHOTO_REVIEW"
            elif watchers > 0:
                state, priority, action = "WATCHED_NO_SALE", "P1_REVENUE_OPPORTUNITY", "OFFER_REVIEW_IF_MARGIN_OK"
            elif days >= 14:
                state, priority, action = "REBUILD_CANDIDATE", "P2_REFRESH_NEEDED", "REBUILD_OR_REPLACE_REVIEW"
            elif days >= 7:
                state, priority, action = "REFRESH_CANDIDATE", "P2_REFRESH_NEEDED", "PHOTO_ORDER_TITLE_REFRESH"
            else:
                state, priority, action = "MONITOR", "P3_MONITOR", "NO_ACTION"

            summary[state] = summary.get(state, 0) + 1
            rows.append(HealthRow(sku, listing_id, days, price, qty, views, watchers, sales, ad_rate, state, priority, action))

        return ListingHealthDashboardResult(
            status="PASS",
            rows=[asdict(x) for x in rows],
            summary=summary,
            next_allowed_action="REVIEW_DASHBOARD_WITH_OPERATOR",
        )
