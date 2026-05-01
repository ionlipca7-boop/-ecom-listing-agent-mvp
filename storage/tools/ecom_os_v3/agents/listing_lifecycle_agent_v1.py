from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class ListingLifecycleDecision:
    sku: str
    listing_id: str
    days_live: int
    health_state: str
    recommended_action: str
    reasons: List[str]
    required_gates: List[str]


@dataclass
class ListingLifecycleResult:
    status: str
    decisions: List[Dict[str, Any]]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ListingLifecycleAgentV1:
    """Deterministic post-listing lifecycle strategy agent.

    It recommends only. It never revises, promotes, discounts, ends, or deletes listings.
    """

    def run(self, listings: List[Dict[str, Any]]) -> ListingLifecycleResult:
        decisions: List[ListingLifecycleDecision] = []
        for item in listings:
            sku = str(item.get("sku") or "UNKNOWN_SKU")
            listing_id = str(item.get("listing_id") or "UNKNOWN_LISTING")
            days = int(item.get("days_live") or 0)
            views = int(item.get("views") or 0)
            watchers = int(item.get("watchers") or 0)
            sales = int(item.get("sales") or 0)
            impressions = int(item.get("impressions") or 0)
            ad_spend = float(item.get("ad_spend") or 0)

            reasons: List[str] = []
            gates: List[str] = ["TELEGRAM_OPERATOR_REVIEW"]

            if sales > 0:
                state = "HEALTHY_SELLING"
                action = "KEEP_MONITORING"
                reasons.append("sales_present")
            elif days < 3:
                state = "NEW_UNDER_OBSERVATION"
                action = "WAIT_FOR_EARLY_SIGNAL"
                reasons.append("listing_too_new")
            elif impressions < 50 and days >= 3:
                state = "IMPRESSIONS_LOW"
                action = "TITLE_KEYWORD_REVIEW_CANDIDATE"
                reasons.append("low_impressions")
                gates += ["COMPETITOR_SNAPSHOT", "CRITIC_PASS"]
            elif views < 10 and days >= 5:
                state = "VIEWS_LOW"
                action = "MAIN_PHOTO_AND_TITLE_REVIEW_CANDIDATE"
                reasons.append("low_views_after_5_days")
                gates += ["COMPETITOR_SNAPSHOT", "CRITIC_PASS"]
            elif watchers > 0 and sales == 0:
                state = "WATCHED_NO_SALE"
                action = "OFFER_5_PERCENT_CANDIDATE_IF_MARGIN_OK"
                reasons.append("watchers_present_no_sale")
                gates += ["MARGIN_CHECK"]
            elif ad_spend > 0 and sales == 0 and days >= 7:
                state = "AD_SPEND_NO_SALE"
                action = "AD_RATE_OR_LISTING_REBUILD_REVIEW"
                reasons.append("ad_spend_without_sale")
                gates += ["MARGIN_CHECK", "COMPETITOR_SNAPSHOT"]
            elif days >= 14:
                state = "REBUILD_CANDIDATE"
                action = "REBUILD_OR_REPLACE_DRAFT_CANDIDATE"
                reasons.append("stale_after_14_days")
                gates += ["ARCHIVE_CURRENT_STATE", "OPERATOR_APPROVAL"]
            elif days >= 7:
                state = "REFRESH_CANDIDATE"
                action = "PHOTO_ORDER_TITLE_REFRESH_CANDIDATE"
                reasons.append("no_sale_after_7_days")
                gates += ["CRITIC_PASS"]
            else:
                state = "MONITOR"
                action = "NO_ACTION"
                reasons.append("no_strong_signal")

            decisions.append(ListingLifecycleDecision(sku, listing_id, days, state, action, reasons, gates))

        return ListingLifecycleResult(
            status="PASS",
            decisions=[asdict(x) for x in decisions],
            next_allowed_action="REVIEW_LIFECYCLE_DECISIONS_WITH_OPERATOR",
        )
