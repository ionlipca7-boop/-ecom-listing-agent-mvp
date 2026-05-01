from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class PromotionOfferDecision:
    sku: str
    listing_id: str
    ad_rate_action: str
    offer_action: str
    margin_status: str
    reasons: List[str]
    required_gates: List[str]


@dataclass
class PromotionOffersResult:
    status: str
    decisions: List[Dict[str, Any]]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PromotionOffersAgentV1:
    """Recommends ad/offers strategy only. No live changes."""

    def run(self, listings: List[Dict[str, Any]]) -> PromotionOffersResult:
        out: List[PromotionOfferDecision] = []
        for item in listings:
            sku = str(item.get("sku") or "UNKNOWN_SKU")
            listing_id = str(item.get("listing_id") or "UNKNOWN_LISTING")
            watchers = int(item.get("watchers") or 0)
            sales = int(item.get("sales") or 0)
            days = int(item.get("days_live") or 0)
            ad_rate = float(item.get("ad_rate") or 0)
            ad_spend = float(item.get("ad_spend") or 0)
            margin_known = bool(item.get("margin_known"))
            min_margin_ok = bool(item.get("minimum_margin_ok"))
            reasons: List[str] = []
            gates: List[str] = ["TELEGRAM_OPERATOR_REVIEW"]

            if not margin_known:
                margin_status = "BLOCKED_MARGIN_UNKNOWN"
                ad_action = "NO_AD_CHANGE"
                offer_action = "NO_OFFER"
                reasons.append("margin_unknown")
                gates.append("MARGIN_CHECK_REQUIRED")
            elif not min_margin_ok:
                margin_status = "BLOCKED_MARGIN_TOO_LOW"
                ad_action = "NO_AD_INCREASE"
                offer_action = "NO_DISCOUNT"
                reasons.append("minimum_margin_not_ok")
            else:
                margin_status = "PASS_MARGIN_OK"
                if ad_rate == 0:
                    ad_action = "START_7_PERCENT_CANDIDATE" if days >= 0 else "NO_AD_CHANGE"
                    reasons.append("baseline_ad_rate_candidate")
                elif ad_rate < 7:
                    ad_action = "RAISE_TO_7_PERCENT_CANDIDATE"
                    reasons.append("below_baseline_ad_rate")
                elif 7 <= ad_rate < 9 and days >= 7 and ad_spend > 0 and sales == 0:
                    ad_action = "RAISE_TO_9_PERCENT_REVIEW_CANDIDATE"
                    reasons.append("weak_ad_result_after_7_days")
                elif 9 <= ad_rate < 10 and days >= 10 and ad_spend > 0 and sales == 0:
                    ad_action = "RAISE_TO_10_PERCENT_REVIEW_OR_REBUILD"
                    reasons.append("weak_ad_result_after_10_days")
                else:
                    ad_action = "KEEP_AD_RATE"
                    reasons.append("ad_rate_ok")

                if watchers > 0 and sales == 0:
                    offer_action = "OFFER_5_PERCENT_CANDIDATE"
                    reasons.append("watchers_no_sale")
                    gates.append("OFFER_ELIGIBILITY_CHECK")
                else:
                    offer_action = "NO_OFFER"

            out.append(PromotionOfferDecision(sku, listing_id, ad_action, offer_action, margin_status, reasons, gates))

        return PromotionOffersResult(
            status="PASS",
            decisions=[asdict(x) for x in out],
            next_allowed_action="REVIEW_PROMOTION_OFFER_DECISIONS_WITH_OPERATOR",
        )
