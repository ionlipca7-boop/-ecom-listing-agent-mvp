from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class MarketplaceRulesResult:
    status: str
    marketplace: str
    language: str
    photo_rules: Dict[str, Any]
    listing_rules: Dict[str, Any]
    blocked_reasons: List[str]
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MarketplaceRulesAgentV1:
    """Loads deterministic marketplace rules for local sandbox.

    Current project default: eBay Germany. This is not legal advice and does not
    replace current marketplace policy review before live actions.
    """

    def run(self, marketplace: str = "ebay_de") -> MarketplaceRulesResult:
        m = (marketplace or "ebay_de").lower()
        blocked: List[str] = []
        if m not in {"ebay_de", "ebay_germany"}:
            blocked.append("unsupported_marketplace_for_v1")

        return MarketplaceRulesResult(
            status="PASS" if not blocked else "BLOCKED",
            marketplace="ebay_de",
            language="de_only",
            photo_rules={
                "main_image_clean": True,
                "second_image_clean": True,
                "main_image_no_text": True,
                "main_image_no_watermark": True,
                "main_image_no_border": True,
                "secondary_images_german_callouts_allowed_if_truthful": True,
                "default_photo_count": "8-12",
                "human_visual_review_required": True,
            },
            listing_rules={
                "title_language": "German",
                "html_language": "German",
                "unsupported_claims_forbidden": True,
                "brand_unknown_must_be_neutral": True,
                "price_quantity_protected_until_scope_approved": True,
                "live_action_requires_gate": True,
            },
            blocked_reasons=blocked,
            next_allowed_action="PRODUCT_PASSPORT_OR_CRITIC" if not blocked else "FIX_MARKETPLACE_PROFILE",
        )
